@echo off
REM ============================================
REM PhotoSite Folder Structure Setup
REM Run this from: P:\Users\marko\Local\PhotoSite\PhotoSite\
REM ============================================

echo Creating organized asset structure...

REM Main asset directories
mkdir assets\images 2>nul
mkdir assets\css 2>nul
mkdir assets\js 2>nul
mkdir assets\images\hero 2>nul
mkdir assets\images\ui 2>nul

REM Gallery structure with thumbnails and full-res separation
REM Collection 1: Big Bend 2025
mkdir "assets\images\gallery\big-bend-2025" 2>nul
mkdir "assets\images\gallery\big-bend-2025\thumbnails" 2>nul
mkdir "assets\images\gallery\big-bend-2025\full-res" 2>nul

REM Collection 2: Colorado Springs Rodeo 2025
mkdir "assets\images\gallery\colorado-rodeo-2025" 2>nul
mkdir "assets\images\gallery\colorado-rodeo-2025\thumbnails" 2>nul
mkdir "assets\images\gallery\colorado-rodeo-2025\full-res" 2>nul

REM Collection 3: Action Sports (your 5 individual images)
mkdir "assets\images\gallery\action-sports" 2>nul
mkdir "assets\images\gallery\action-sports\thumbnails" 2>nul
mkdir "assets\images\gallery\action-sports\full-res" 2>nul

REM Future collections (create as needed)
REM mkdir "assets\images\gallery\nature" 2>nul
REM mkdir "assets\images\gallery\portraits" 2>nul

echo.
echo Folder structure created successfully!
echo.
echo Next steps:
echo 1. Move your existing JPGs into the appropriate full-res folders
echo 2. Generate thumbnails using the provided Python script
echo 3. Create metadata.json files in each gallery folder
echo.
pause
