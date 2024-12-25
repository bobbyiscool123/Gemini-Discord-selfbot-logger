import discord
import time
import google.generativeai as genai
import asyncio
import tkinter as tk
import threading
import platform
import pyscreenshot as ImageGrab
from PIL import Image
import io
import os
import vlc  # Import python-vlc
import traceback
from dotenv import load_dotenv
# import playsound

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables, with default values if not found
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_USER_TOKEN = os.getenv("DISCORD_USER_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
SOUND_FILE_PATH = os.getenv("SOUND_FILE_PATH", r"C:\Users\PRAD\Downloads\chime.mp3")  # Default chime sound path

print(f"GEMINI_API_KEY: {GEMINI_API_KEY}")
print(f"DISCORD_USER_TOKEN: {DISCORD_USER_TOKEN}")
print(f"GROUP_CHAT_ID: {GROUP_CHAT_ID}")
print(f"SOUND_FILE_PATH: {SOUND_FILE_PATH}")

def play_system_sound(sound_file):
    try:
        instance = vlc.Instance()
        media = instance.media_new(sound_file)
        player = instance.media_player_new()
        player.set_media(media)
        player.play()
        while player.is_playing():
            time.sleep(0.1)
    except Exception as e:
       print(f"Error playing sound with VLC: {e}")
       traceback.print_exc()
       # try:
            # playsound.playsound(sound_file)
       # except Exception as e:
           # print(f"Error playing sound with playsound: {e}")
           # traceback.print_exc()


# --- Gemini Setup ---
gemini_api_key = GEMINI_API_KEY

if not gemini_api_key:
    print("Gemini API key not found. Set the GEMINI_API_KEY environment variable in .env file.")
    exit()

try:
    genai.configure(api_key=gemini_api_key)
except Exception as e:
    print(f"An error occurred during Gemini setup: {e}")
    traceback.print_exc()
    exit()

generation_config = {
    "temperature": 1.75,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="analyze and send it as a java script error  and do not share private information & tell it as what bobby is doing right now and also make it only 100 words humour 100% must as an error code please it should look like an error code  ",
)

# --- Discord Setup ---
discord_token = DISCORD_USER_TOKEN
if not discord_token:
    print("Discord user token not found. Set the DISCORD_USER_TOKEN environment variable in .env file.")
    exit()

group_chat_id = os.getenv("GROUP_CHAT_ID")
if not group_chat_id:
    print("Group chat ID is not set. Please set the GROUP_CHAT_ID in the .env file.")
    exit()
try:
    group_chat_id = int(group_chat_id)
except ValueError:
    print("Group chat ID is not a valid integer. Please correct the GROUP_CHAT_ID in the .env file.")
    exit()



message_windows = {}
is_window_open = False
client = discord.Client()


def create_message_window(message_contents):
    global is_window_open
    if is_window_open:
        return  # only create a new window if old one is not open
    is_window_open = True

    def run_window():
        window = tk.Tk()
        window.title("Multiple Messages")
        text_area = tk.Text(window, wrap="word")
        text_area.pack(padx=10, pady=10, expand=True, fill="both")

        for content in message_contents:
            text_area.insert(tk.END, content + "\n\n")

        timer_label = tk.Label(window, text="0.000s")
        timer_label.pack(pady=20)
        start_time = time.time()

        def update_timer():
             if is_window_open:  # check if window is still open
                elapsed_time = time.time() - start_time
                timer_label.config(text=f"{elapsed_time:.3f}s")
                window.after(10, update_timer)

        def on_window_close():
            global is_window_open
            is_window_open = False
            window.destroy()
            if "multi_message_window" in message_windows:
                del message_windows["multi_message_window"]

        update_timer()
        window.protocol("WM_DELETE_WINDOW", on_window_close)  # Set close event handler
        message_windows["multi_message_window"] = window
        window.mainloop()

    thread = threading.Thread(target=run_window)
    thread.daemon = True
    thread.start()


async def capture_screenshot():
    try:
        screenshot = ImageGrab.grab()  # Take a full-screen screenshot
        return screenshot
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        traceback.print_exc()
        return None


async def generate_gemini_reply(screenshot_image):

    chat_history = [{"role": "user", "parts": []}]
    
    if screenshot_image:
      try:
        # Convert the PIL Image to bytes
        img_byte_arr = io.BytesIO()
        screenshot_image.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()
        
        # Prepare the image part
        image_part = {
            "mime_type": "image/png",
            "data": img_byte_arr
        }
        chat_history[0]['parts'].append(image_part)
      except Exception as e:
            print(f"Error processing screenshot for Gemini: {e}")
            traceback.print_exc()
            return "An error occurred while processing the screenshot for your request."


    chat_session = model.start_chat(history=chat_history)

    try:
        response = await chat_session.send_message_async(content="Analyze this image") #This fixes the error
        gemini_reply = response.text
        return gemini_reply
    except Exception as e:
        print(f"Error generating Gemini reply: {e}")
        traceback.print_exc()
        return "An error occurred while processing your request."


async def send_periodic_updates():
    await client.wait_until_ready()
    channel = client.get_channel(group_chat_id)
    while not client.is_closed():
      start_time = time.time()

      screenshot_image = await capture_screenshot()

      gemini_reply = await generate_gemini_reply(screenshot_image)

      end_time = time.time()
      elapsed_time = end_time - start_time

      formatted_elapsed_time = f"{elapsed_time:.2f}s"
      if gemini_reply:
        print(f"Gemini reply: {gemini_reply}")
        await channel.send(f"```console```\n{gemini_reply}```\nGemini Flash-2.0-Exp {formatted_elapsed_time}```")

        play_system_sound(SOUND_FILE_PATH)

        create_message_window([f"Gemini Reply: {gemini_reply}"])
      else:
        print("Error: No Gemini Reply generated.")
      await asyncio.sleep(60)  # wait for 60 seconds


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(send_periodic_updates())


if __name__ == "__main__":
    try:
      client.run(discord_token)
    except discord.errors.LoginFailure as e:
      print(f"Discord Login Failure: {e}. Please check your bot token.")
      traceback.print_exc()