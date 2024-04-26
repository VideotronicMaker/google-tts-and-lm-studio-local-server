# Basic Instructions

The primary file to execute is `kitt_g_voice.py`.

The batch file, `run_script.bat`, simplifies running the Python program without the need for multiple Command Prompt commands. It prompts you to activate your designated workspace, sets the file paths, and then executes the program. This saves time and simplifies the process, eliminating the need to manually enter commands. Keep both files in the same folder as `kitt_g_voice.py`. Make sure to rename `"myenv"` in the batch file to match the name of your Python environment. You can create a desktop shortcut for quick access and customize its icon for easier identification.

## Usage Note:

Please note that the method for starting the local server provided in this repository may not work on all systems or operating systems due to variations in dependencies and system configurations. Additionally, changes or updates to the OpenAI Whisper and or Openai libraries may affect the functionality of the code provided here.Users are encouraged to be aware of potential issues and to consult their GPT (Generative Pre-trained Transformer) for assistance when encountering problems. The initial code in this repository was developed with the help of ChatGPT, and users are encouraged to utilize similar resources for troubleshooting and finding solutions to any issues they may encounter.Furthermore, it's important to regularly check and update the requirements.txt file to ensure compatibility with different versions of dependencies.

The `system_message.txt` file is used for providing custom instructions to the model, known as a system prompt or pre-prompt. Keep this file in the same folder.

Store your `GOOGLE_APPLICATION_CREDENTIALS` file securely. Copy the file path and paste it into the `run_script.bat` file.

# Google Cloud Setup for Text-to-Speech

To enable Google Cloud Text-to-Speech functionality:

1. Create a Google Cloud Project if you haven't already (https://console.cloud.google.com).
2. Enable the Text-to-Speech API within your project.
3. Create a new service account in your project with the "Text-to-Speech Client" role.
4. Download the JSON file containing your service account's API key credentials. Keep this file secure and do not include it in your GitHub repository.
5. Set the environment variable:

**Windows:**
set GOOGLE_APPLICATION_CREDENTIALS=D:\path\to\your\key.json

**MacOS/Linux:**
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/key.json

Replace placeholders with your actual paths.

**Security Reminder:** The JSON key file contains sensitive information. Never commit it to public version control like GitHub. Explore secure credential management strategies in Google Cloud documentation for production environments.

Need help with anything?:

Remeber to utilize GPT 4 or Gemini Ultra.  This entire project was created with those products.

For additional assistance, refer to Google Cloud's documentation:

- [Creating & Managing Service Accounts](https://cloud.google.com/iam/docs/creating-managing-service-accounts)
- [Authentication Basics](https://cloud.google.com/docs/authentication/getting-started)


