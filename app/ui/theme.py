"""Color/theme presets -- vivid, modern palettes (default: Aurora) plus the
classic IDE themes and one light option.

Every preset carries, beyond the base surface/text colours, an `accent`
(a second saturated hue for highlights and the deep-dive difficulty), a
`gradient` pair (hero banners, primary tiles) and a `surface` (a card
sitting on a card). The motion/component layers read only these fields,
so a new preset is one entry here and nothing else."""
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
    accent: str = "#F472B6"
    """Second saturated hue: highlights, the deep-dive badge, confetti."""
    gradient: tuple[str, str] = ("#4F46E5", "#DB2777")
    """Start/end colours for hero banners and primary tiles."""
    surface: str = "#2A2F3A"
    """A raised surface inside a card (code blocks, pills, option rows)."""
    shadow: str = "#000000"
    """Base colour for drop shadows (alpha is applied at use)."""


THEME_PRESETS: dict[str, ThemePreset] = {
    "aurora": ThemePreset(
        key="aurora", title="Aurora", icon="\U0001F30C", is_dark=True,
        bg="#0B1020", card="#151B2E", text="#E6EAF5", text_muted="#8B95B5",
        primary="#8B8CFF", primary_hover="#6E6FE8",
        success="#34D399", success_hover="#22B583",
        warning="#FBBF24", danger="#FB7185",
        accent="#F472B6", gradient=("#6366F1", "#EC4899"), surface="#1E2640",
    ),
    "sunset": ThemePreset(
        key="sunset", title="Sunset", icon="\U0001F305", is_dark=True,
        bg="#1A1023", card="#261833", text="#FCEFF6", text_muted="#B49BC2",
        primary="#FF8A65", primary_hover="#F4703F",
        success="#7ED9A6", success_hover="#5FC48F",
        warning="#FFD166", danger="#FF5D8F",
        accent="#C084FC", gradient=("#F97316", "#DB2777"), surface="#332042",
    ),
    "ocean": ThemePreset(
        key="ocean", title="Ocean", icon="\U0001F30A", is_dark=True,
        bg="#06131F", card="#0E1F2F", text="#DDF3FF", text_muted="#7FA7BF",
        primary="#38BDF8", primary_hover="#1FA7E4",
        success="#2DD4BF", success_hover="#14B8A6",
        warning="#FACC15", danger="#FB7185",
        accent="#A78BFA", gradient=("#0EA5E9", "#14B8A6"), surface="#153047",
    ),
    "one_dark": ThemePreset(
        key="one_dark", title="One Dark", icon="\U0001F311", is_dark=True,
        bg="#282C34", card="#21252B", text="#ABB2BF", text_muted="#5C6370",
        primary="#61AFEF", primary_hover="#4A93D4",
        success="#98C379", success_hover="#7FAE62",
        warning="#E5C07B", danger="#E06C75",
        accent="#C678DD", gradient=("#61AFEF", "#C678DD"), surface="#2C313A",
    ),
    "dracula": ThemePreset(
        key="dracula", title="Dracula", icon="\U0001F9DB", is_dark=True,
        bg="#282A36", card="#21222C", text="#F8F8F2", text_muted="#6272A4",
        primary="#BD93F9", primary_hover="#A57EE0",
        success="#50FA7B", success_hover="#3FDB68",
        warning="#F1FA8C", danger="#FF5555",
        accent="#FF79C6", gradient=("#BD93F9", "#FF79C6"), surface="#343746",
    ),
    "solarized_dark": ThemePreset(
        key="solarized_dark", title="Solarized Dark", icon="\U0001F313", is_dark=True,
        bg="#002B36", card="#073642", text="#93A1A1", text_muted="#586E75",
        primary="#268BD2", primary_hover="#1E6FA8",
        success="#859900", success_hover="#6C7D00",
        warning="#B58900", danger="#DC322F",
        accent="#D33682", gradient=("#268BD2", "#2AA198"), surface="#0B4552",
    ),
    "monokai": ThemePreset(
        key="monokai", title="Monokai", icon="\U0001F5A5️", is_dark=True,
        bg="#272822", card="#1E1F1A", text="#F8F8F2", text_muted="#75715E",
        primary="#66D9EF", primary_hover="#4FC2D8",
        success="#A6E22E", success_hover="#8FC91E",
        warning="#E6DB74", danger="#F92672",
        accent="#AE81FF", gradient=("#66D9EF", "#AE81FF"), surface="#2F302A",
    ),
    "github_light": ThemePreset(
        key="github_light", title="GitHub Light", icon="☀️", is_dark=False,
        bg="#F6F8FA", card="#FFFFFF", text="#24292F", text_muted="#57606A",
        primary="#0969DA", primary_hover="#0757BA",
        success="#1A7F37", success_hover="#166A2E",
        warning="#9A6700", danger="#CF222E",
        accent="#8250DF", gradient=("#0969DA", "#8250DF"), surface="#EEF1F5", shadow="#1B1F24",
    ),
}

DEFAULT_THEME_KEY = "aurora"


def get_preset(theme_key: str) -> ThemePreset:
    return THEME_PRESETS.get(theme_key, THEME_PRESETS[DEFAULT_THEME_KEY])


FONT_SIZE_SCALES: dict[str, float] = {"small": 0.9, "medium": 1.0, "large": 1.15}
DEFAULT_FONT_SIZE_KEY = "medium"

CODE_FONT_FAMILY = "Consolas, 'Courier New', monospace"


def resolve_font_scale(key: str) -> float:
    return FONT_SIZE_SCALES.get(key, FONT_SIZE_SCALES[DEFAULT_FONT_SIZE_KEY])


def scaled(base_size: int, scale: float) -> int:
    return max(1, round(base_size * scale))
