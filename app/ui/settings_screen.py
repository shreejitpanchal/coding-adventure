"""Settings: theme presets (live-preview swatch cards), code font size,
Daily Refresher size, and progress backup/restore."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

import flet as ft

from app.ui.app_state import AppState
from app.ui.components import RADIUS, button, card, header_row, route_handler, spacer, tint, view_padding
from app.ui.motion import Stagger, glow, hover_lift
from app.ui.theme import FONT_SIZE_SCALES, THEME_PRESETS, ThemePreset, scaled

logger = logging.getLogger(__name__)


def build_settings_view(page: ft.Page, state: AppState) -> ft.View:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    stagger = Stagger(page)

    back_route = "/hub" if state.language else "/languages"
    header = header_row(theme, fs, "Settings", route_handler(page, back_route), icon=ft.Icons.SETTINGS_ROUNDED,
                        subtitle="Make it yours -- every change applies instantly")

    controls: list[ft.Control] = [
        header, spacer(8),
        stagger.wrap(_build_theme_card(page, state)),
        stagger.wrap(_build_font_card(page, state)),
        stagger.wrap(_build_daily_refresher_card(page, state)),
        stagger.wrap(_build_weekly_goal_card(page, state)),
        stagger.wrap(_build_backup_card(page, state)),
    ]
    stagger.play()

    return ft.View(
        route="/settings",
        bgcolor=theme.bg,
        scroll=ft.ScrollMode.AUTO,
        padding=view_padding(page),
        controls=controls,
    )


_FONT_SIZE_LABELS = {"small": "Small", "medium": "Medium", "large": "Large", "xlarge": "Extra large"}
_DAILY_REFRESHER_SIZE_CHOICES = [3, 5, 8, 10]
_WEEKLY_GOAL_CHOICES = [5, 10, 15, 25, 40]


def _rebuild(page: ft.Page, state: AppState) -> None:
    """Re-render this screen in place after a setting changed, so the new
    theme/font is visible immediately without a route change."""
    page.views.clear()
    page.views.append(build_settings_view(page, state))
    page.bgcolor = state.theme.bg
    page.theme_mode = ft.ThemeMode.DARK if state.theme.is_dark else ft.ThemeMode.LIGHT
    page.update()


def _segmented(theme, options: list[tuple[str, str]], current: str, on_pick) -> ft.Row:
    """A row of pill buttons where the current one is filled."""
    return ft.Row(
        [
            button(label, on_pick(key), theme, "primary" if current == key else "ghost", height=40, disabled=current == key)
            for key, label in options
        ],
        wrap=True, spacing=8,
    )


def _build_font_card(page: ft.Page, state: AppState) -> ft.Control:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    def select(size_key: str):
        def handler(_e=None) -> None:
            state.apply_font_size(size_key)
            _rebuild(page, state)
        return handler

    preview = ft.Column(
        [
            ft.Text("Heading preview", size=fs(20), weight=ft.FontWeight.BOLD, color=theme.text),
            ft.Text("Body text scales with this setting on every screen, on desktop and phone.",
                    size=fs(14), color=theme.text_muted),
            ft.Text("def refresh(skills): return sorted(skills, key=len)", size=fs(14), color=theme.text,
                    font_family="Consolas, 'Courier New', monospace"),
        ],
        spacing=6,
    )
    return card(theme, fs, "Text size", [
        ft.Text("Applies everywhere: headings, body text, chips, code editors and output.",
                size=fs(13), color=theme.text_muted),
        _segmented(theme, [(k, _FONT_SIZE_LABELS.get(k, k)) for k in FONT_SIZE_SCALES], state.settings.code_font_size, select),
        ft.Container(content=preview, bgcolor=theme.surface, border_radius=10, padding=12),
    ], icon=ft.Icons.TEXT_FIELDS_ROUNDED, accent=theme.primary, title_size=18, margin_top=4)


def _build_daily_refresher_card(page: ft.Page, state: AppState) -> ft.Control:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    def select(size: int):
        def handler(_e=None) -> None:
            state.apply_daily_refresher_size(size)
            _rebuild(page, state)
        return handler

    current = state.settings.daily_refresher_size
    return card(theme, fs, "Daily Refresher size", [
        ft.Text(
            "How many exercises show up in a Daily Refresher round. Takes effect "
            "the next time a fresh set is generated -- today's set, if you've "
            "already started it, stays as-is.",
            size=fs(13), color=theme.text_muted,
        ),
        ft.Row(
            [
                button(str(size), select(size), theme, "primary" if current == size else "ghost", height=40, width=64,
                       disabled=current == size)
                for size in _DAILY_REFRESHER_SIZE_CHOICES
            ],
            wrap=True, spacing=8,
        ),
    ], icon=ft.Icons.TODAY_ROUNDED, accent=theme.warning, title_size=18, margin_top=4)


def _build_weekly_goal_card(page: ft.Page, state: AppState) -> ft.Control:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    def select(goal: int):
        def handler(_e=None) -> None:
            state.apply_weekly_goal(goal)
            _rebuild(page, state)
        return handler

    current = state.settings.weekly_goal
    return card(theme, fs, "Weekly goal", [
        ft.Text(
            "Exercises to complete per week (Monday to Sunday, your local time). Shown on the hub and the "
            "Progress screen for whichever track you're in.",
            size=fs(13), color=theme.text_muted,
        ),
        ft.Row(
            [
                button(str(goal), select(goal), theme, "primary" if current == goal else "ghost", height=40, width=64,
                       disabled=current == goal)
                for goal in _WEEKLY_GOAL_CHOICES
            ],
            wrap=True, spacing=8,
        ),
    ], icon=ft.Icons.FLAG_ROUNDED, accent=theme.success, title_size=18, margin_top=4)


def _build_theme_card(page: ft.Page, state: AppState) -> ft.Control:
    theme = state.theme
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731
    current_key = state.settings.theme

    options = [
        ft.Container(content=_build_theme_option(page, state, preset, current_key == preset.key),
                     col={"xs": 12, "sm": 6, "md": 4, "lg": 3})
        for preset in THEME_PRESETS.values()
    ]
    return card(theme, fs, "Theme", [
        ft.Text("Each swatch is drawn in its own palette -- pick the one that feels right.", size=fs(13), color=theme.text_muted),
        ft.ResponsiveRow(options, spacing=14, run_spacing=14),
    ], icon=ft.Icons.PALETTE_ROUNDED, accent=theme.accent, title_size=18, margin_top=4)


def _build_theme_option(page: ft.Page, state: AppState, preset: ThemePreset, is_selected: bool) -> ft.Control:
    fs = lambda base: scaled(base, state.font_scale)  # noqa: E731

    def select(_e=None) -> None:
        state.apply_theme(preset.key)
        _rebuild(page, state)

    swatches = ft.Row(
        [ft.Container(bgcolor=color, width=22, height=22, border_radius=6)
         for color in (preset.primary, preset.accent, preset.success, preset.warning, preset.danger)],
        spacing=6,
    )
    mini_hero = ft.Container(
        height=34, border_radius=8,
        gradient=ft.LinearGradient(colors=[preset.gradient[0], preset.gradient[1]]),
    )
    option = ft.Container(
        content=ft.Column(
            [
                ft.Row([
                    ft.Text(f"{preset.icon} {preset.title}", size=fs(15), weight=ft.FontWeight.BOLD, color=preset.text, expand=True),
                    ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=preset.primary, size=fs(20)) if is_selected else ft.Container(),
                ]),
                mini_hero,
                swatches,
                ft.Text("Selected" if is_selected else "Tap to apply", size=fs(11),
                        color=preset.primary if is_selected else preset.text_muted),
            ],
            spacing=10,
        ),
        bgcolor=preset.bg, border_radius=RADIUS - 2, padding=16,
        border=ft.Border.all(3 if is_selected else 1, preset.primary if is_selected else tint(preset.text, 0.15)),
        on_click=None if is_selected else select, ink=not is_selected,
        shadow=glow(preset.primary, alpha=0.4) if is_selected else None,
    )
    return hover_lift(option, state.theme, glow_color=preset.primary) if not is_selected else option


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
        status_text.color = theme.danger if is_error else theme.success
        page.update()

    async def save_export_to_device(payload: bytes, filename: str) -> None:
        picker = ft.FilePicker()
        try:
            saved_path = await picker.save_file(
                dialog_title="Export Progress", file_name=filename, src_bytes=payload,
            )
        except Exception as e:  # native dialogs can raise platform-specific errors
            logger.exception("Export file dialog failed")
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
            logger.exception("Share sheet failed")
            set_status(f"Share failed: {e}", is_error=True)
            return
        set_status("Shared." if result.status == ft.ShareResultStatus.SUCCESS else "Share cancelled.")

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
                button("Save to Device", choose_save, theme, "primary", icon=ft.Icons.SAVE_ROUNDED),
                button("Share…", choose_share, theme, "success", icon=ft.Icons.UPLOAD_ROUNDED),
                button("Cancel", close, theme, "ghost"),
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
                logger.warning("Progress import of %s rejected: %s", picked_file.name, e)
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
            title=ft.Row([ft.Icon(ft.Icons.ERROR_OUTLINE_ROUNDED, color=theme.danger),
                          ft.Text("Replace all progress?", size=fs(18), weight=ft.FontWeight.BOLD, color=theme.danger)],
                         spacing=10),
            content=ft.Text(
                f'Importing "{picked_file.name}" will permanently replace your current '
                "progress across every track -- XP, streaks, completions, and achievements "
                "all included -- with what's in this file. This can't be undone. Continue?",
                size=fs(13), color=theme.text,
            ),
            actions=[
                button("Import & Overwrite", confirm, theme, "danger", icon=ft.Icons.DOWNLOAD_ROUNDED),
                button("Cancel", close, theme, "ghost"),
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
            logger.exception("Import file dialog failed")
            set_status(f"Import failed: {e}", is_error=True)
            return
        if not files:
            return
        show_import_confirmation(files[0])

    return card(theme, fs, "Backup & Restore", [
        ft.Text(
            "Export every track's XP, streaks, completions, and achievements as a "
            "JSON file, or restore from a previous export -- importing replaces all "
            "current progress, so you'll be asked to confirm first.",
            size=fs(13), color=theme.text_muted,
        ),
        ft.Row(
            [
                button("Export Progress", on_export, theme, "primary", icon=ft.Icons.UPLOAD_ROUNDED),
                button("Import Progress", on_import, theme, "ghost", icon=ft.Icons.DOWNLOAD_ROUNDED),
            ],
            spacing=10, wrap=True,
        ),
        status_text,
    ], icon=ft.Icons.SAVE_ROUNDED, accent=theme.success, title_size=18, margin_top=4)
