@echo off

echo Installing requirements...
pip install -r requirements.txt
pip install pyinstaller

echo Building Windows executable...
pyinstaller --onefile --windowed --name=RedditBotDashboard main.py

echo.
echo Done! Check the 'dist' folder for RedditBotDashboard.exe
pause
