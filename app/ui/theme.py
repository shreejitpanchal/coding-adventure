"""Color/theme presets -- professional dark-IDE palettes plus one light option."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ThemePreset:
    key: str
    title: str
    icon: str
    is_dark: bool
    bg: str
    card: str
    text: str
    text_muted: str
    primary: str
    primary_hover: str
    success: str
    success_hover: str
    warning: str
    danger: str


THEME_PRESETS: dict[str, ThemePreset] = {
    "one_dark": ThemePreset(
        key="one_dark", title="One Dark", icon="\U0001F311", is_dark=True,
        bg="#282C34", card="#21252B", text="#ABB2BF", text_muted="#5C6370",
        primary="#61AFEF", primary_hover="#4A93D4",
        success="#98C379", success_hover="#7FAE62",
        warning="#E5C07B", danger="#E06C75",
    ),
    "dracula": ThemePreset(
        key="dracula", title="Dracula", icon="\U0001F9DB", is_dark=True,
        bg="#282A36", card="#21222C", text="#F8F8F2", text_muted="#6272A4",
        primary="#BD93F9", primary_hover="#A57EE0",
        success="#50FA7B", success_hover="#3FDB68",
        warning="#F1FA8C", danger="#FF5555",
    ),
    "solarized_dark": ThemePreset(
        key="solarized_dark", title="Solarized Dark", icon="\U0001F313", is_dark=True,
        bg="#002B36", card="#073642", text="#93A1A1", text_muted="#586E75",
        primary="#268BD2", primary_hover="#1E6FA8",
        success="#859900", success_hover="#6C7D00",
        warning="#B58900", danger="#DC322F",
    ),
    "monokai": ThemePreset(
        key="monokai", title="Monokai", icon="\U0001F5A5️", is_dark=True,
        bg="#272822", card="#1E1F1A", text="#F8F8F2", text_muted="#75715E",
        primary="#66D9EF", primary_hover="#4FC2D8",
        success="#A6E22E", success_hover="#8FC91E",
        warning="#E6DB74", danger="#F92672",
    ),
    "github_light": ThemePreset(
        key="github_light", title="GitHub Light", icon="☀️", is_dark=False,
        bg="#FFFFFF", card="#F6F8FA", text="#24292F", text_muted="#57606A",
        primary="#0969DA", primary_hover="#0757BA",
        success="#1A7F37", success_hover="#166A2E",
        warning="#9A6700", danger="#CF222E",
    ),
}

DEFAULT_THEME_KEY = "one_dark"


def get_preset(theme_key: str) -> ThemePreset:
    return THEME_PRESETS.get(theme_key, THEME_PRESETS[DEFAULT_THEME_KEY])


FONT_SIZE_SCALES: dict[str, float] = {"small": 0.9, "medium": 1.0, "large": 1.15}
DEFAULT_FONT_SIZE_KEY = "medium"

CODE_FONT_FAMILY = "Consolas, 'Courier New', monospace"


def resolve_font_scale(key: str) -> float:
    return FONT_SIZE_SCALES.get(key, FONT_SIZE_SCALES[DEFAULT_FONT_SIZE_KEY])


def scaled(base_size: int, scale: float) -> int:
    return max(1, round(base_size * scale))
