from pyrogram import Client, filters, idle
import asyncio

# Replace these with your actual API ID, API HASH, and BOT TOKEN
API_ID = 22420997  # Replace with your actual API ID
API_HASH = "d7fbe2036e9ed2a1468fad5a5584a255"  # Replace with your actual API hash
BOT_TOKEN = "7176424785:AAEusrLtmtGgRisJ6Pje6yAnN-ZbdZMoO1Q"  # Replace with your actual bot token

# Create a Pyrogram client using the bot token
app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start"))
def start(client, message):
    client.send_message(message.chat.id, "Hello! I am a bot to save restricted content. Send me the post link.")

@app.on_message(filters.text)
def save_restricted_content(client, message):
    if "https://t.me/" in message.text:
        # Split the message text to get the channel/user and message ID
        datas = message.text.split("/")
        username = datas[3]  # username or chat id
        msg_id = int(datas[-1])  # message ID

        try:
            msg = client.get_messages(username, msg_id)
            # Downloading and sending the message
            if msg:
                if msg.media:
                    client.send_media_group(message.chat.id, [msg.media])
                else:
                    client.send_message(message.chat.id, msg.text)
        except Exception as e:
            client.send_message(message.chat.id, f"Error: {str(e)}")

async def main():
    await app.start()
    print("Bot is running...")
    await idle()  # Keep the bot running

if __name__ == "__main__":
    asyncio.run(main())
