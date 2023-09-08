@echo off
setlocal

set QT_REPO_DIR=externals\Qt6
set QT_BUILD_DIR=externals\Qt6\qt6-build
set LIB_DIR=lib\Qt6

set FORCE_CLONE=0
set SHOW_HELP=0

:arg_loop
if "%~1"=="" goto end_arg_loop
if "%~1"=="--force-clone" set FORCE_CLONE=1
if "%~1"=="--help" set SHOW_HELP=1
shift
goto arg_loop
:end_arg_loop

if %SHOW_HELP%==1 (
    echo Usage: script-name [options]
    echo.
    echo Options:
    echo  --force-clone  Remove the existing Qt6 directory and clone it again.
    echo  --help         Show this help message.
    exit /b 0
)

if %FORCE_CLONE%==1 (
    if exist "%QT_REPO_DIR%" (
        rmdir /s /q "%QT_REPO_DIR%"
    )
)

if not exist "%QT_REPO_DIR%\*" (
    mkdir "%QT_REPO_DIR%"
    if errorlevel 1 (
        echo "Error: Could not create directory %QT_REPO_DIR%."
        exit /b 1
    )
    git clone git@github.com:qt/qt5.git "%QT_REPO_DIR%"
    cd "%QT_REPO_DIR%"
    git checkout v6.3.0
    cd "%CD%"
) else (
    echo "Directory %QT_REPO_DIR% already exists. Skipping repository cloning."
)

cd %QT_REPO_DIR%

perl init-repository --module-subset=qtbase,qtnetworkauth
if errorlevel 1 (
    echo "Error: Failed to initialize the repository."
    exit /b 1
)

mkdir qt6-build
if errorlevel 1 (
    echo "Error: Could not create qt6-build directory."
    exit /b 1
)
cd qt6-build

call ..\configure.bat -prefix ..\..\..\%LIB_DIR%
if errorlevel 1 (
    echo "Error: Failed to run the configure script."
    exit /b 1
)

cmake --build .
if errorlevel 1 (
    echo "Error: Failed to build the project."
    exit /b 1
)

cmake --install .
if errorlevel 1 (
    echo "Error: Failed to install the project."
    exit /b 1
)

echo "Operation completed successfully."
endlocal
