from pyrogram import Client, filters, idle
import asyncio

API_ID = 22420997  # Replace with your actual API ID
API_HASH = "d7fbe2036e9ed2a1468fad5a5584a255"  # Replace with your actual API hash
BOT_TOKEN = "7490926656:AAHG-oUUzGPony9xfyApSI0EbbymhneDU1k"  # Replace with your actual bot token

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start"))
def start(client, message):
    print("Received /start command")  # Debug print
    client.send_message(message.chat.id, "Hello! I am a bot to save restricted content. Send me the post link.")

async def main():
    await app.start()
    print("Bot is running...")  # Confirm bot is running
    await idle()  # Keep the bot running

if __name__ == "__main__":
    asyncio.run(main())
