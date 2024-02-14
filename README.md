# Basic Instructions

The main file is the "kitt_g_voice.py"

The "run_script.bat" file is for quickly running the application in your terminal without having to type all of the cmds over and over each time you run the file.  Keep this file in the same folder as the "kitt_g_voice.py" file.

The "system_message.txt" file is where you can give the model custom instructions also known as a system prompt or pre-prompt.  Keep this file in the same folder also.

Put your GOOGLE_APPLICATION_CREDENTIALS file somewhere else for security.  Copy the path to wherever you put it and pste the path into the "run_script.bat" file.


# Google Cloud Setup for Text-to-Speech

For the Google Cloud Text-to-Speech functionality to work within this script, please complete the following:

Google Cloud Project and Service Account:

If you don't have one, create a Google Cloud Project (https://console.cloud.google.com).
Enable the Text-to-Speech API within your project (instructions in Google Cloud documentation).
Create a new service account in your project, granting it the "Text-to-Speech Client" role.
Download API Key File (JSON):

Download the JSON file containing your service account's API key credentials.
Safely store this file on your local machine; do not include it in the GitHub repository.
Set Environment Variable:

Windows:

Open Command Prompt.
Execute this command, replacing placeholders with your actual paths:
Bash
set GOOGLE_APPLICATION_CREDENTIALS=D:\path\to\your\key.json 
Use code with caution.
MacOS/Linux:

Open a terminal.
Execute this command, replacing placeholders with your actual paths:
Bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/key.json
Use code with caution.
Security Reminder:

The JSON key file holds sensitive information. Never commit it to public version control like GitHub.
Consider exploring more secure credential management strategies found in the Google Cloud documentation for production environments.
Need Further Help?

Refer to Google Cloud's documentation for  more assistance:

Creating & Managing Service Accounts: https://cloud.google.com/iam/docs/creating-managing-service-accounts
Authentication Basics: https://cloud.google.com/docs/authentication/getting-started
