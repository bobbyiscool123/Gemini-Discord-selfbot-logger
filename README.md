# Discord Self-Bot Logger with Gemini AI

This Python script is a self-bot that uses the Gemini AI model to analyze screenshots and then sends a humorous interpretation of what's happening on screen as a simulated JavaScript error code to a Discord group chat periodically.

**Important Disclaimer:**

*   Using self-bots is **against Discord's Terms of Service** and may result in your account being banned. Use this at your own risk.
*   This script is designed for educational purposes and personal experimentation. Do not use this in any way that could violate platform terms, privacy, or cause harm.

## Features

*   **Gemini AI Integration:** Utilizes the Google Gemini API to analyze screenshots.
*   **Discord Integration:** Sends updates to a Discord group chat at regular intervals.
*   **Humorous Error-Like Output:**  Presents the analysis as a humorous fake JavaScript error.
*   **Screenshot Capture:** Takes a screenshot of your screen using `pyscreenshot`.
*   **Pop-Up Window:** Displays the Gemini analysis in a pop-up window.
*   **Notification Sound:** Plays a sound when updates are sent, using `vlc`.
*   **Environment Variable Configuration:** Loads all necessary tokens and IDs from a `.env` file, enhancing security and flexibility.

## Prerequisites

1.  **Python 3.7+**

2.  **Install Required Libraries:**

    ```bash
    pip install discord.py google-generativeai python-dotenv pyscreenshot Pillow python-vlc
    ```
    If `python-vlc` is causing problems try `pip install playsound` and use that library as an alternative.

3.  **Google Gemini API Key:** You will need an API key from Google Gemini.
    *  Get yours here [Google Gemini API](https://makersuite.google.com/app/apikey)

4.  **Discord User Token:** You will need your Discord user token.
    *   **Do not share your user token with anyone.**
    *  To get your token log into the Discord Web app in Google Chrome. Open `Developer Tools`, go to the `Application` tab, then the `Local Storage` section, you should see a field called `token`. Copy this value.

5.  **Discord Group Chat ID:** The ID of the group chat in Discord where you want the bot to send messages.
  * Enable developer mode by navigating to Discord's `Settings` > `Advanced`.
   * In the Discord app, right click on the desired channel or group chat and click `Copy ID`

6.  **Sound File:** Optionally include a sound file to play as a notification.

## Setup

1.  **Create a `.env` file** in the same directory as the Python script. This file will store your API keys and tokens.
   * To create the file right-click in the file explorer and create a new text file, rename it to `.env`. Ensure that the file has no file extension (e.g. `.env.txt`).

2.  **Populate the `.env` file** with the following content, replacing the placeholders with your actual values:

    ```
    GEMINI_API_KEY=your_gemini_api_key
    DISCORD_USER_TOKEN=your_discord_user_token
    GROUP_CHAT_ID=your_discord_channel_id
    SOUND_FILE_PATH=C:\path\to\your\sound.mp3
    ```
    *   Replace `your_gemini_api_key`, `your_discord_user_token`, `your_discord_channel_id`, and `C:\path\to\your\sound.mp3` with your actual API key, token, channel ID, and sound file path.
    *   Ensure that there are no extra white spaces after each line in the file.

3.  **Run the Script:**
    ```bash
    python your_script_name.py
    ```

## How It Works

1.  The script loads configuration settings from the `.env` file.
2.  It initializes the Gemini API and the Discord client using the provided keys.
3.  It runs in a loop:
    *   Takes a screenshot of the screen.
    *   Sends the screenshot to the Gemini AI model for analysis.
    *   Receives a response from Gemini AI.
    *   Sends the humorous error-like response to the specified Discord group chat.
    *   Plays a notification sound.
    *   Displays a pop-up window showing the response.
    *   Waits for 60 seconds before repeating the process.
4.  If any errors occur, details of the error are printed to the terminal.

## Error Handling

*   The script includes error handling for:
    *   Invalid environment variables.
    *   Gemini API setup or request failures.
    *   Discord login or message sending failures.
    *   Screenshot errors.
    *  VLC playback errors.

## Additional Notes

*   The script uses threads for the tkinter window, allowing the program to continue running while the window is open.
*   Be cautious about rate-limiting with Discord. The current interval is 60 seconds. Do not reduce the interval too much.
*   The script is designed for personal learning purposes.
*   Ensure the user running the script has the necessary OS permissions for screenshotting and playing sounds.
*  The current implementation utilizes a `python-vlc` for sound playback, if this causes problems consider using `playsound` as an alternative.
*  The script generates "humorous javascript error codes" as requested in the system prompt, you may change this as you wish in the script.

## Disclaimer

*   The use of self-bots violates Discord's Terms of Service, and your account may be banned.
*   Use this code responsibly and at your own risk.

This README.md provides a comprehensive overview of your code's functionality, setup, and potential risks. Please adapt it to reflect any future changes in your code.