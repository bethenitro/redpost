@echo off
echo Building Windows executable...

pip install pyinstaller
pyinstaller --onefile --windowed --name=RedditBotDashboard main.py

echo.
echo Done! Check the 'dist' folder for RedditBotDashboard.exe
pause
