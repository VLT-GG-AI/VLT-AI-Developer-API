@echo off
setlocal enabledelayedexpansion
title VLT GG AI Updater

echo ----------------------------------------------
echo          VLT GG AI - DELTA UPDATER
echo ----------------------------------------------
echo.

:: Location of your installed client
set INSTALL_DIR=%cd%

echo Current directory:
echo   %INSTALL_DIR%
echo.

echo Pulling latest update from GitHub...
echo.

:: Download newest repo as ZIP
curl -L -o update.zip "https://github.com/VLT-GG-AI/VLT-AI-Developer-API/archive/refs/heads/main.zip"

if not exist update.zip (
    echo ERROR: Could not download update.
    pause
    exit /b
)

echo.
echo Extracting update package...

powershell -command "Expand-Archive -LiteralPath 'update.zip' -DestinationPath '.' -Force"

if not exist "VLT-AI-Developer-API-main" (
    echo ERROR: Extraction failed. ZIP may be corrupt.
    pause
    exit /b
)

echo.
echo Copying updated files to install directory...

xcopy "VLT-AI-Developer-API-main\*.*" "%INSTALL_DIR%\" /E /Y >nul

echo.
echo Cleaning temporary update files...

del update.zip >nul
rmdir /S /Q "VLT-AI-Developer-API-main" >nul

echo.
echo ----------------------------------------------
echo            UPDATE COMPLETE!
echo ----------------------------------------------
echo.

set /p runnow=Launch VLTGG AI now? (Y/N):

if /I "%runnow%"=="Y" (
    echo.
    python client.py
)

exit /b
