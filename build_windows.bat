@echo off
REM Builds EmberTournament.exe on a Windows PC.  Needs Python 3.10+ (python.org, "Add python.exe to PATH" ticked).
REM Result:  dist\EmberTournament\EmberTournament.exe   (zip the whole EmberTournament folder to share it)
cd /d "%~dp0"
python -m venv .buildenv || (echo Python was not found & pause & exit /b 1)
.buildenv\Scripts\python -m pip install -q -r requirements.txt pyinstaller || (echo Install failed & pause & exit /b 1)
.buildenv\Scripts\pyinstaller --noconfirm --clean --windowed --name EmberTournament --icon icon.ico --add-data "data;data" --collect-all pygame main.py || (echo Build failed & pause & exit /b 1)
echo.
echo DONE.  Play with:  dist\EmberTournament\EmberTournament.exe
pause
