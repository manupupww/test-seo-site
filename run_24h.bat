@echo off
:loop
python main.py
timeout /t 21600 /nobreak > nul
goto loop