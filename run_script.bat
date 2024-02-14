@echo off

echo Activating Conda environment...
call conda activate python

echo Changing directory... 
cd \path\to\your folder

echo Setting Google Credentials...
set GOOGLE_APPLICATION_CREDENTIALS=\path\to\your folder\your file name here.json

REM Specify the path to your conda.exe (adjust if necessary)
set CONDA_EXE=C:\Users\YourUserName\Anaconda3\Scripts\conda.exe

%CONDA_EXE% activate python

echo Running Python script...
%YOUR_ENV_NAME% sparkle_g_voice.py
pause