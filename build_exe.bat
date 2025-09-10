@echo off
echo Building Reddit Bot executable...

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM Install/upgrade required packages
pip install --upgrade -r requirements.txt

REM Build with PyInstaller using spec file
pyinstaller reddit_bot.spec

REM Check if build was successful
if exist "dist\RedditBot.exe" (
    echo.
    echo ✅ Build successful! 
    echo Executable created: dist\RedditBot.exe
    echo.
    echo You can now run the executable from the dist folder.
    pause
) else (
    echo.
    echo ❌ Build failed! Check the output above for errors.
    pause
)