from pyrogram import Client, filters, idle
import asyncio
from flask import Flask
import threading

API_ID = 22420997  # Replace with your actual API ID
API_HASH = "d7fbe2036e9ed2a1468fad5a5584a255"  # Replace with your actual API hash
BOT_TOKEN = "7176424785:AAEusrLtmtGgRisJ6Pje6yAnN-ZbdZMoO1Q"  # Replace with your actual bot token

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Flask app setup
flask_app = Flask(__name__)

@flask_app.route('/')
def hello():
    return 'Hello, World!'  # Ensure no non-printable characters are present

@app.on_message(filters.command("start"))
def start(client, message):
    print("Received /start command")  # Debug print
    client.send_message(message.chat.id, "Hello! I am a bot to save restricted content. Send me the post link.")

async def run_bot():
    await app.start()
    print("Bot is running...")  # Confirm bot is running
    await idle()  # Keep the bot running

def run_flask():
    # Run the Flask app on port 10000
    flask_app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    # Start the bot in a separate thread
    threading.Thread(target=run_flask).start()
    asyncio.run(run_bot())
