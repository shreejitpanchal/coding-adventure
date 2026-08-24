@echo off
REM Checks whether Java (javac/java) and a C++ compiler (g++) are on PATH,
REM and -- only with the user's explicit y/n confirmation, asked separately
REM for each -- offers to install whichever is missing via winget (Windows'
REM built-in package manager). Safe to call on every launch: it's a no-op
REM once both are already installed, and never installs anything without
REM an explicit "y" typed at the prompt.
REM
REM Intended to be `call`ed from run_app_window_mode.bat / run_app_web_ui.bat,
REM not run directly.

where javac >nul 2>nul
if errorlevel 1 call :offer_install_java

where g++ >nul 2>nul
if errorlevel 1 call :offer_install_cpp

exit /b 0

:offer_install_java
setlocal
where winget >nul 2>nul
if errorlevel 1 (
    echo.
    echo Java ^(JDK^) was not found, and winget isn't available on this
    echo computer to install it automatically. Install it manually -- see
    echo the "Toolchain needed" guide on the language picker in the app.
    endlocal
    exit /b 0
)

echo.
echo ============================================
echo   Java ^(JDK^) was not found on this computer.
echo   Coding Adventure can install it automatically
echo   using Windows' built-in winget package manager.
echo ============================================
set /p INSTALL_JAVA="Install Java now? [y/N] "
if /i not "%INSTALL_JAVA%"=="y" (
    echo Skipping Java install -- the Java/Spring tracks will show
    echo "Toolchain needed" until it's installed.
    endlocal
    exit /b 0
)

echo Installing Java via winget, this may take a minute...
winget install --id EclipseAdoptium.Temurin.21.JDK -e --accept-package-agreements --accept-source-agreements
if errorlevel 1 (
    echo Something went wrong installing Java. Install it manually instead --
    echo see the "Toolchain needed" guide on the language picker in the app.
) else (
    echo Java installed. Close and reopen this terminal, then run this
    echo script again for the change to take effect ^(Windows doesn't
    echo update an already-open terminal's PATH^).
)
endlocal
exit /b 0

:offer_install_cpp
setlocal
where winget >nul 2>nul
if errorlevel 1 (
    echo.
    echo A C++ toolchain ^(g++^) was not found, and winget isn't available
    echo on this computer to install it automatically. Install it manually
    echo -- see the "Toolchain needed" guide on the language picker in the app.
    endlocal
    exit /b 0
)

echo.
echo ============================================
echo   A C++ toolchain ^(g++^) was not found on this computer.
echo   Coding Adventure can install MSYS2 and its
echo   mingw-w64 g++ compiler automatically.
echo ============================================
set /p INSTALL_CPP="Install a C++ toolchain now? [y/N] "
if /i not "%INSTALL_CPP%"=="y" (
    echo Skipping C++ toolchain install -- the C++ track will show
    echo "Toolchain needed" until it's installed.
    endlocal
    exit /b 0
)

if not exist "C:\msys64\usr\bin\bash.exe" (
    echo Installing MSYS2 via winget, this may take a minute...
    winget install --id MSYS2.MSYS2 -e --accept-package-agreements --accept-source-agreements
    if errorlevel 1 (
        echo Something went wrong installing MSYS2. Install a C++ toolchain
        echo manually instead -- see the "Toolchain needed" guide on the
        echo language picker in the app.
        endlocal
        exit /b 0
    )
)

if exist "C:\msys64\usr\bin\bash.exe" (
    echo Installing the mingw-w64 g++ compiler inside MSYS2...
    "C:\msys64\usr\bin\bash.exe" -lc "pacman -Sy --noconfirm mingw-w64-x86_64-gcc"

    echo Adding C:\msys64\mingw64\bin to your PATH...
    powershell -NoProfile -Command "$p = [Environment]::GetEnvironmentVariable('Path','User'); if ($p -notlike '*C:\msys64\mingw64\bin*') { [Environment]::SetEnvironmentVariable('Path', $p + ';C:\msys64\mingw64\bin', 'User') }"

    echo C++ toolchain installed. Close and reopen this terminal, then run
    echo this script again for the change to take effect ^(Windows doesn't
    echo update an already-open terminal's PATH^).
) else (
    echo MSYS2 installation did not complete as expected. Install a C++
    echo toolchain manually instead -- see the "Toolchain needed" guide on
    echo the language picker in the app.
)
endlocal
exit /b 0
