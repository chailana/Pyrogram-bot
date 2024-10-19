from pyrogram import Client, filters
import os
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace these with your values from .env
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
STRING_SESSION = os.getenv('STRING_SESSION')

# Initialize the bot and user clients
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_client = Client("user", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

# Start user client
async def start_user_client():
    await user_client.start()

# Function to download media
async def download_media(chat_id, message_id):
    try:
        message = await user_client.get_messages(chat_id, message_id)
        if message.media:
            file_path = await user_client.download_media(message.media)
            return file_path
    except Exception as e:
        print(f"Error downloading media: {e}")
    return None

# Function to upload media
async def upload_media(chat_id, file_path):
    try:
        await bot.send_document(chat_id, file_path)
        os.remove(file_path)  # Remove the file after sending
    except Exception as e:
        print(f"Error uploading media: {e}")

# Command handler for starting the bot
@bot.on_message(filters.command("start"))
async def start(event):
    await event.reply("Hi! I can download and upload restricted content from public and private channels/groups.\nSend a link in the format:\n`https://t.me/channel/1-100` for batch processing.")

# Command handler for processing links
@bot.on_message(filters.text)
async def handle_message(event):
    if 'https://t.me/' in event.message.text:
        url = event.message.text.strip()
        batch_match = re.search(r'https://t.me/([^/]+)/(\d+)-(\d+)', url)

        if batch_match:
            channel = batch_match.group(1)
            start_id = int(batch_match.group(2))
            end_id = int(batch_match.group(3))

            # Use ThreadPoolExecutor for concurrent downloading
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
                futures = [loop.run_in_executor(executor, download_media, channel, message_id) for message_id in range(start_id, end_id + 1)]
                downloaded_files = await asyncio.gather(*futures)

            # Upload downloaded media concurrently
            upload_futures = [upload_media(event.chat.id, file) for file in downloaded_files if file]
            await asyncio.gather(*upload_futures)

        else:
            # Single message handling
            try:
                chat_id = url.split('/')[-2]
                message_id = int(url.split('/')[-1])
                file_path = await download_media(chat_id, message_id)
                if file_path:
                    await upload_media(event.chat.id, file_path)
                else:
                    await bot.send_message(event.chat.id, f"Failed to download message {message_id} from {chat_id}.")
            except Exception as e:
                print(f"Error: {e}")

# Start the clients
async def main():
    await start_user_client()
    await bot.run()

if __name__ == '__main__':
    asyncio.run(main())
