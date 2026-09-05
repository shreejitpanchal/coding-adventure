"""Settings: theme presets, code font size, and progress backup/restore."""
from __future__ import annotations

import json
from datetime import datetime, timezone

import flet as ft

from app.ui.app_state import AppState
from app.ui.theme import FONT_SIZE_SCALES, THEME_PRESETS, ThemePreset, scaled


def build_settings_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    back_route = "/hub" if state.language else "/languages"

    header = ft.Row(
        [
            ft.Button(
                "← Back", on_click=lambda _e: page.go(back_route), height=44,
                style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF"),
            ),
            ft.Text("Settings", size=fs(24), weight=ft.FontWeight.BOLD, color=theme.primary, expand=True),
        ],
        spacing=12,
    )

    return ft.View(
        route="/settings",
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=ft.padding.Padding.only(left=24, top=24, right=24, bottom=40),
        controls=[
            header, _build_font_card(page, state), _build_theme_card(page, state),
            _build_backup_card(page, state),
        ],
    )


_FONT_SIZE_LABELS = {"small": "Small", "medium": "Medium", "large": "Large"}


def _build_font_card(page: ft.Page, state: AppState) -> ft.Control:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    def select(size_key: str):
        def handler(_e=None) -> None:
            state.apply_font_size(size_key)
            page.views.clear()
            page.views.append(build_settings_view(page, state))
            page.update()
        return handler

    current = state.settings.code_font_size
    buttons = [
        ft.Button(
            label, on_click=select(key), height=40, disabled=current == key,
            style=ft.ButtonStyle(bgcolor=theme.primary if current == key else theme.text_muted, color="#FFFFFF"),
        )
        for key in FONT_SIZE_SCALES for label in [_FONT_SIZE_LABELS.get(key, key)]
    ]

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Code font size", size=fs(18), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Row(buttons, wrap=True, spacing=8),
            ],
            spacing=10,
        ),
        bgcolor=theme.card, border_radius=16, padding=20, margin=ft.margin.Margin.only(top=16),
    )


def _build_theme_card(page: ft.Page, state: AppState) -> ft.Control:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    current_key = state.settings.theme

    options = [_build_theme_option(page, state, preset, current_key == preset.key) for preset in THEME_PRESETS.values()]

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Theme", size=fs(18), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Row(options, wrap=True, spacing=16, run_spacing=16),
            ],
            spacing=10,
        ),
        bgcolor=theme.card, border_radius=16, padding=20, margin=ft.margin.Margin.only(top=16),
    )


def _build_theme_option(page: ft.Page, state: AppState, preset: ThemePreset, is_selected: bool) -> ft.Control:
    def select(_e=None) -> None:
        state.apply_theme(preset.key)
        page.views.clear()
        page.views.append(build_settings_view(page, state))
        page.bgcolor = state.theme.bg
        page.theme_mode = ft.ThemeMode.DARK if state.theme.is_dark else ft.ThemeMode.LIGHT
        page.update()

    swatches = ft.Row(
        [ft.Container(bgcolor=color, width=24, height=24, border_radius=6) for color in (preset.primary, preset.success, preset.warning, preset.danger)],
        spacing=6,
    )

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(f"{preset.icon} {preset.title}", size=scaled(15, state.font_scale), weight=ft.FontWeight.BOLD, color=preset.text),
                swatches,
                ft.Button(
                    "Selected" if is_selected else "Select", disabled=is_selected, on_click=select, height=40,
                    style=ft.ButtonStyle(bgcolor=preset.primary, color="#FFFFFF"),
                ),
            ],
            spacing=8,
        ),
        bgcolor=preset.bg, border_radius=14, padding=16, width=220,
        border=ft.border.Border.all(3, state.theme.primary if is_selected else preset.card),
    )


def _export_filename() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"coding_adventure_progress_{stamp}.json"


def _build_backup_card(page: ft.Page, state: AppState) -> ft.Control:
    """Export/import every track's progress (XP, streaks, completions,
    achievements) as one JSON file -- a full backup/restore, not scoped to
    the currently-selected track, since ProgressStore.export_progress()
    covers every language at once. Export offers a plain "save to device"
    file dialog everywhere, plus a native platform Share sheet on mobile
    (Flet's Share service) so the file can be handed off to whichever app
    the user picks there, including their mail client -- there's no way to
    target one specific app like Gmail directly without a share sheet the
    OS itself controls, so this hands the choice to the OS's own picker
    rather than assuming Gmail is installed or hardcoding it as a target."""
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    status_text = ft.Text("", size=fs(12), color=theme.text_muted)

    def set_status(message: str, is_error: bool = False) -> None:
        status_text.value = message
        status_text.color = theme.danger if is_error else theme.text_muted
        page.update()

    async def save_export_to_device(payload: bytes, filename: str) -> None:
        picker = ft.FilePicker()
        try:
            saved_path = await picker.save_file(
                dialog_title="Export Progress", file_name=filename, src_bytes=payload,
            )
        except Exception as e:  # native dialogs can raise platform-specific errors
            set_status(f"Export failed: {e}", is_error=True)
            return
        set_status(f"Saved to {saved_path}." if saved_path else "Export cancelled.")

    async def share_export(payload: bytes, filename: str) -> None:
        sharer = ft.Share()
        try:
            result = await sharer.share_files(
                [ft.ShareFile.from_bytes(payload, mime_type="application/json", name=filename)],
                subject="Coding Adventure progress backup",
                text="Attached: a Coding Adventure progress export.",
            )
        except Exception as e:
            set_status(f"Share failed: {e}", is_error=True)
            return
        set_status(
            "Shared." if result.status == ft.ShareResultStatus.SUCCESS else "Share cancelled."
        )

    def show_mobile_export_choice(payload: bytes, filename: str) -> None:
        def close(_e: ft.ControlEvent | None = None) -> None:
            page.pop_dialog()

        def choose_save(_e: ft.ControlEvent) -> None:
            close()
            page.run_task(save_export_to_device, payload, filename)

        def choose_share(_e: ft.ControlEvent) -> None:
            close()
            page.run_task(share_export, payload, filename)

        page.show_dialog(ft.AlertDialog(
            modal=False,
            bgcolor=theme.card,
            title=ft.Text("Export Progress", size=fs(18), weight=ft.FontWeight.BOLD, color=theme.text),
            content=ft.Text(
                "Save the backup file on this device, or share it through any app that "
                "accepts files -- including your mail app, if you'd rather email yourself "
                "a copy (e.g. as a Gmail attachment) than save it locally.",
                size=fs(13), color=theme.text_muted,
            ),
            actions=[
                ft.Button("Save to Device", on_click=choose_save,
                          style=ft.ButtonStyle(bgcolor=theme.primary, color="#FFFFFF")),
                ft.Button("Share…", on_click=choose_share,
                          style=ft.ButtonStyle(bgcolor=theme.success, color="#FFFFFF")),
                ft.Button("Cancel", on_click=close,
                          style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF")),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        ))

    async def on_export(_e: ft.ControlEvent) -> None:
        payload = json.dumps(state.progress.export_progress(), indent=2, ensure_ascii=False).encode("utf-8")
        filename = _export_filename()
        if page.platform.is_mobile():
            show_mobile_export_choice(payload, filename)
        else:
            await save_export_to_device(payload, filename)

    def show_import_confirmation(picked_file: ft.FilePickerFile) -> None:
        def close(_e: ft.ControlEvent | None = None) -> None:
            page.pop_dialog()

        def confirm(_e: ft.ControlEvent) -> None:
            close()
            try:
                raw = picked_file.bytes
                if raw is None:
                    raise ValueError("the selected file couldn't be read")
                data = json.loads(raw.decode("utf-8"))
                state.progress.import_progress(data)
            except Exception as e:
                set_status(f"Import failed: {e}", is_error=True)
                return
            # Every track's progress just changed under this session -- send
            # the user back to the language picker so every screen (hub, XP,
            # streaks, unlocked levels) rebuilds fresh against the new data,
            # rather than leaving stale numbers on screen until navigated away.
            page.go("/languages")

        page.show_dialog(ft.AlertDialog(
            modal=True,
            bgcolor=theme.card,
            title=ft.Text("Replace all progress?", size=fs(18), weight=ft.FontWeight.BOLD, color=theme.danger),
            content=ft.Text(
                f'Importing "{picked_file.name}" will permanently replace your current '
                "progress across every track -- XP, streaks, completions, and achievements "
                "all included -- with what's in this file. This can't be undone. Continue?",
                size=fs(13), color=theme.text,
            ),
            actions=[
                ft.Button("Import & Overwrite", on_click=confirm,
                          style=ft.ButtonStyle(bgcolor=theme.danger, color="#FFFFFF")),
                ft.Button("Cancel", on_click=close,
                          style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF")),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        ))

    async def on_import(_e: ft.ControlEvent) -> None:
        picker = ft.FilePicker()
        try:
            files = await picker.pick_files(
                dialog_title="Import Progress",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=["json"],
                with_data=True,
            )
        except Exception as e:
            set_status(f"Import failed: {e}", is_error=True)
            return
        if not files:
            return
        show_import_confirmation(files[0])

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Backup & Restore", size=fs(18), weight=ft.FontWeight.BOLD, color=theme.text),
                ft.Text(
                    "Export every track's XP, streaks, completions, and achievements as a "
                    "JSON file, or restore from a previous export -- importing replaces all "
                    "current progress, so you'll be asked to confirm first.",
                    size=fs(13), color=theme.text_muted,
                ),
                ft.Row(
                    [
                        ft.Button("⬆ Export Progress", on_click=on_export, height=44,
                                  style=ft.ButtonStyle(bgcolor=theme.primary, color="#FFFFFF")),
                        ft.Button("⬇ Import Progress", on_click=on_import, height=44,
                                  style=ft.ButtonStyle(bgcolor=theme.text_muted, color="#FFFFFF")),
                    ],
                    spacing=10, wrap=True,
                ),
                status_text,
            ],
            spacing=10,
        ),
        bgcolor=theme.card, border_radius=16, padding=20, margin=ft.margin.Margin.only(top=16),
    )
