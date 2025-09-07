@echo off
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt
pip install pyinstaller

echo Building Windows executable...
pyinstaller --onefile --windowed --name=RedditBotDashboard main.py

echo.
echo Done! Check the 'dist' folder for RedditBotDashboard.exe
pause
