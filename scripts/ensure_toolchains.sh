#!/usr/bin/env bash
# Checks whether Java (javac/java) and a C++ compiler (g++) are on PATH,
# and -- only with the user's explicit y/n confirmation, asked separately
# for each -- offers to install whichever is missing via the platform's
# own package manager (winget on Windows-via-Git-Bash, Homebrew on macOS,
# apt/dnf/pacman on Linux). Safe to run on every launch: it's a no-op once
# both are already installed, and never installs anything without an
# explicit "y" typed at the prompt.
#
# Intended to be run as its own process from run_app_window_mode.sh /
# run_app_web_ui.sh (e.g. `bash scripts/ensure_toolchains.sh || true`),
# not sourced -- so a failed/declined install here never aborts the
# caller, even under `set -e`.

_os_name() {
    case "$(uname -s)" in
        Darwin) echo "macos" ;;
        Linux) echo "linux" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *) echo "other" ;;
    esac
}

_confirm() {
    # $1 = prompt text. Defaults to "no" on anything but y/yes.
    read -r -p "$1 [y/N] " REPLY
    case "$REPLY" in
        [yY]|[yY][eE][sS]) return 0 ;;
        *) return 1 ;;
    esac
}

_windows_path_add() {
    # $1 = directory to append to the user PATH, via PowerShell (avoids
    # the ~1024-char truncation risk of `setx`).
    powershell.exe -NoProfile -Command \
        "\$p = [Environment]::GetEnvironmentVariable('Path','User'); if (\$p -notlike '*$1*') { [Environment]::SetEnvironmentVariable('Path', \$p + ';$1', 'User') }"
}

ensure_java() {
    command -v javac >/dev/null 2>&1 && return 0

    echo
    echo "============================================"
    echo "  Java (JDK) was not found on this computer."
    echo "============================================"

    local os
    os="$(_os_name)"

    case "$os" in
        macos)
            if ! command -v brew >/dev/null 2>&1; then
                echo "Coding Adventure uses Homebrew to install Java on macOS, but Homebrew"
                echo "isn't installed. Install it first from https://brew.sh, then run this"
                echo "script again."
                return 0
            fi
            if _confirm "Install Java now via Homebrew (brew install openjdk)?"; then
                brew install openjdk
                echo "Java installed. Follow brew's own PATH-linking instructions above,"
                echo "then open a new terminal and run this script again."
            else
                echo "Skipping Java install -- the Java/Spring tracks will show \"Toolchain needed\" until it's installed."
            fi
            ;;
        linux)
            if command -v apt >/dev/null 2>&1; then
                if _confirm "Install Java now via apt (sudo apt install default-jdk)?"; then
                    sudo apt update && sudo apt install -y default-jdk
                else
                    echo "Skipping Java install -- the Java/Spring tracks will show \"Toolchain needed\" until it's installed."
                fi
            elif command -v dnf >/dev/null 2>&1; then
                if _confirm "Install Java now via dnf (sudo dnf install java-latest-openjdk-devel)?"; then
                    sudo dnf install -y java-latest-openjdk-devel
                else
                    echo "Skipping Java install -- the Java/Spring tracks will show \"Toolchain needed\" until it's installed."
                fi
            elif command -v pacman >/dev/null 2>&1; then
                if _confirm "Install Java now via pacman (sudo pacman -S jdk-openjdk)?"; then
                    sudo pacman -S --noconfirm jdk-openjdk
                else
                    echo "Skipping Java install -- the Java/Spring tracks will show \"Toolchain needed\" until it's installed."
                fi
            else
                echo "No supported package manager (apt/dnf/pacman) found -- install a JDK manually from https://adoptium.net"
            fi
            ;;
        windows)
            if ! command -v winget.exe >/dev/null 2>&1; then
                echo "winget isn't available on this computer to install Java automatically."
                echo "Install it manually -- see the \"Toolchain needed\" guide on the language picker in the app."
                return 0
            fi
            if _confirm "Install Java now via winget?"; then
                winget.exe install --id EclipseAdoptium.Temurin.21.JDK -e --accept-package-agreements --accept-source-agreements
                echo "Java installed. Close and reopen this terminal, then run this script"
                echo "again for the change to take effect."
            else
                echo "Skipping Java install -- the Java/Spring tracks will show \"Toolchain needed\" until it's installed."
            fi
            ;;
        *)
            echo "Install a JDK manually for your platform -- see https://adoptium.net"
            ;;
    esac
}

ensure_cpp() {
    command -v g++ >/dev/null 2>&1 && return 0

    echo
    echo "============================================"
    echo "  A C++ toolchain (g++) was not found on this computer."
    echo "============================================"

    local os
    os="$(_os_name)"

    case "$os" in
        macos)
            if _confirm "Install the Xcode Command Line Tools now (provides g++/clang)?"; then
                xcode-select --install
                echo "Follow the installer window that just opened, then open a new"
                echo "terminal and run this script again."
            else
                echo "Skipping C++ toolchain install -- the C++ track will show \"Toolchain needed\" until it's installed."
            fi
            ;;
        linux)
            if command -v apt >/dev/null 2>&1; then
                if _confirm "Install a C++ toolchain now via apt (sudo apt install build-essential)?"; then
                    sudo apt update && sudo apt install -y build-essential
                else
                    echo "Skipping C++ toolchain install -- the C++ track will show \"Toolchain needed\" until it's installed."
                fi
            elif command -v dnf >/dev/null 2>&1; then
                if _confirm 'Install a C++ toolchain now via dnf (sudo dnf groupinstall "Development Tools")?'; then
                    sudo dnf groupinstall -y "Development Tools"
                else
                    echo "Skipping C++ toolchain install -- the C++ track will show \"Toolchain needed\" until it's installed."
                fi
            elif command -v pacman >/dev/null 2>&1; then
                if _confirm "Install a C++ toolchain now via pacman (sudo pacman -S base-devel)?"; then
                    sudo pacman -S --noconfirm base-devel
                else
                    echo "Skipping C++ toolchain install -- the C++ track will show \"Toolchain needed\" until it's installed."
                fi
            else
                echo "No supported package manager (apt/dnf/pacman) found -- install a C++ toolchain manually."
            fi
            ;;
        windows)
            if ! command -v winget.exe >/dev/null 2>&1; then
                echo "winget isn't available on this computer to install a C++ toolchain automatically."
                echo "Install it manually -- see the \"Toolchain needed\" guide on the language picker in the app."
                return 0
            fi
            if _confirm "Install MSYS2 + the mingw-w64 g++ compiler now via winget?"; then
                if [ ! -f "/c/msys64/usr/bin/bash.exe" ]; then
                    winget.exe install --id MSYS2.MSYS2 -e --accept-package-agreements --accept-source-agreements
                fi
                if [ -f "/c/msys64/usr/bin/bash.exe" ]; then
                    /c/msys64/usr/bin/bash.exe -lc "pacman -Sy --noconfirm mingw-w64-x86_64-gcc"
                    _windows_path_add 'C:\msys64\mingw64\bin'
                    echo "C++ toolchain installed. Close and reopen this terminal, then run"
                    echo "this script again for the change to take effect."
                else
                    echo "MSYS2 installation did not complete as expected. Install a C++"
                    echo "toolchain manually instead -- see the \"Toolchain needed\" guide"
                    echo "on the language picker in the app."
                fi
            else
                echo "Skipping C++ toolchain install -- the C++ track will show \"Toolchain needed\" until it's installed."
            fi
            ;;
        *)
            echo "Install a C++ toolchain manually for your platform."
            ;;
    esac
}

ensure_java
ensure_cpp
echo
