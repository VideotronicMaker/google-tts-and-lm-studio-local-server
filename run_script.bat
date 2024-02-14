@echo off

echo Activating Conda environment...
call conda activate myenv

echo Changing directory... 
cd /d C:\Path\To\Your\Project

echo Setting Google Credentials...
set GOOGLE_APPLICATION_CREDENTIALS=C:\Path\To\Your\File\yourfilename.json

echo Running Python script...
myenv sparkle_g_voice.py
pause
