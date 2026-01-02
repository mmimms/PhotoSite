@echo off
REM deploy.bat - Local FTP deployment script for PhotoSite
REM Usage: Double-click this file to deploy changes to your live website
REM
REM What it does:
REM   1. Pulls latest code from GitHub (git pull)
REM   2. Syncs changed files to FTP server using WinSCP
REM   3. Credentials stored locally in deploy-config.txt (not in GitHub)

setlocal enabledelayedexpansion

echo.
echo =====================================
echo   PhotoSite - Local FTP Deployment
echo =====================================
echo.

REM Check if config file exists
if not exist "deploy-config.txt" (
    echo.
    echo ❌ ERROR: Config file not found!
    echo.
    echo Please create deploy-config.txt with your FTP credentials
    echo Template:
    echo   FTP_HOST=ftp.yourserver.com
    echo   FTP_USERNAME=your-username
    echo   FTP_PASSWORD=your-password
    echo   FTP_REMOTE_DIR=/public_html/
    echo.
    pause
    exit /b 1
)

REM Read configuration file
echo [Reading credentials from deploy-config.txt...]
for /f "tokens=1,2 delims==" %%a in (deploy-config.txt) do (
    if "%%a"=="FTP_HOST" set FTP_HOST=%%b
    if "%%a"=="FTP_USERNAME" set FTP_USERNAME=%%b
    if "%%a"=="FTP_PASSWORD" set FTP_PASSWORD=%%b
    if "%%a"=="FTP_REMOTE_DIR" set FTP_REMOTE_DIR=%%b
    if "%%a"=="FTP_LOCAL_DIR" set FTP_LOCAL_DIR=%%b
)

if not defined FTP_HOST (
    echo.
    echo ❌ ERROR: FTP_HOST not set in deploy-config.txt
    echo.
    pause
    exit /b 1
)

echo.

REM Step 1: Pull latest from GitHub
echo [STEP 1/3] Pulling latest changes from GitHub...
echo.

git pull origin main

if !errorlevel! neq 0 (
    echo.
    echo ❌ ERROR: Failed to pull from GitHub
    echo Make sure you:
    echo   - Are in the PhotoSite directory
    echo   - Have git installed
    echo   - Have committed your local changes
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ GitHub pull complete
echo.

REM Step 2: Verify WinSCP is installed
echo [STEP 2/3] Preparing FTP sync...
echo.

set WINSCP_PATH=""

if exist "C:\Program Files (x86)\WinSCP\WinSCP.com" (
    set WINSCP_PATH="C:\Program Files (x86)\WinSCP\WinSCP.com"
    echo Found WinSCP: C:\Program Files (x86)\WinSCP
) else if exist "C:\Program Files\WinSCP\WinSCP.com" (
    set WINSCP_PATH="C:\Program Files\WinSCP\WinSCP.com"
    echo Found WinSCP: C:\Program Files\WinSCP
) else (
    echo.
    echo ❌ ERROR: WinSCP not found!
    echo.
    echo WinSCP is required for FTP synchronization.
    echo.
    echo Download it here: https://winscp.net/eng/download.php
    echo Install it, then run this script again.
    echo.
    pause
    exit /b 1
)

echo.
echo FTP Server: !FTP_HOST!
echo Remote Dir: !FTP_REMOTE_DIR!
echo.

REM Create WinSCP synchronization script
echo Creating sync script...
(
    echo open "ftp://!FTP_USERNAME!:!FTP_PASSWORD!@!FTP_HOST!"
    echo cd !FTP_REMOTE_DIR!
    echo option exclude *.md,*.py,.git\*,.gitignore,deploy-config.txt,deploy.bat,sync-script.txt,sync.log
    echo synchronize remote -delete -mirror
    echo exit
) > sync-script.txt

echo.
echo [STEP 3/3] Syncing files to FTP server...
echo.

REM Run WinSCP with the script
!WINSCP_PATH! /console /script=sync-script.txt /log="sync.log" /ini=nul

if !errorlevel! neq 0 (
    echo.
    echo ❌ ERROR: WinSCP sync failed
    echo.
    echo Check your FTP credentials in deploy-config.txt:
    echo   - FTP_HOST
    echo   - FTP_USERNAME
    echo   - FTP_PASSWORD
    echo   - FTP_REMOTE_DIR
    echo.
    echo WinSCP log saved to: sync.log
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ FTP sync complete
echo.

REM Cleanup temporary files
if exist sync-script.txt del sync-script.txt
if exist sync.log del sync.log

echo.
echo =====================================
echo    ✅ DEPLOYMENT SUCCESSFUL!
echo =====================================
echo.
echo Your changes are now live!
echo.
echo Next steps:
echo   - Open your website to verify changes
echo   - Check for any missing images or broken links
echo.

pause
