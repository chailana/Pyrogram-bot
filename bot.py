from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

# Replace these placeholders with your actual values
bot_token = "7176424785:AAEusrLtmtGgRisJ6Pje6yAnN-ZbdZMoO1Q"  # Bot Token
api_hash = "d7fbe2036e9ed2a1468fad5a5584a255"  # API Hash
api_id = 22420997  # API ID

# Initialize the bot client
bot = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Flag to control the ongoing process
is_stopped = False

@bot.on_message(filters.command("start"))
def send_start(client: Client, message):
    bot.send_message(
        message.chat.id,
        f"__👋 Hi **{message.from_user.mention}**, I am Save Restricted Bot, I can send you restricted content by its post link__",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Source Code", url="https://github.com/bipinkrish/Save-Restricted-Bot")]
        ]),
        reply_to_message_id=message.id
    )

@bot.on_message(filters.command("stop"))
def stop_bot(client: Client, message):
    global is_stopped
    is_stopped = True  # Set the flag to stop ongoing processes
    bot.send_message(
        message.chat.id,
        "__🛑 The ongoing process has been stopped. You can start a new process.__",
        reply_to_message_id=message.id
    )

@bot.on_message(filters.text)
async def save(client: Client, message):
    global is_stopped
    print(message.text)

    # Reset the stop flag for new commands
    is_stopped = False

    # Check if the message contains a valid Telegram link
    if "https://t.me/" in message.text:
        try:
            if "-" in message.text:
                await handle_batch_requests(message)
            else:
                await handle_single_message(message)
        except Exception as e:
            await bot.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
    else:
        await bot.send_message(message.chat.id, "Invalid link. Please provide a valid Telegram message link.", reply_to_message_id=message.id)

async def handle_batch_requests(message):
    global is_stopped
    # Extracting the range of message IDs
    try:
        parts = message.text.split("/")
        message_ids = parts[-1].split("-")
        from_id = int(message_ids[0].strip())
        to_id = int(message_ids[1].strip())
        chat_id = parts[-2]  # Extract chat ID from URL

        # Create a list of coroutines for fetching messages
        tasks = [fetch_message(message, msg_id, chat_id) for msg_id in range(from_id, to_id + 1)]
        
        # Execute all tasks concurrently
        await asyncio.gather(*tasks)
    except ValueError as e:
        await bot.send_message(message.chat.id, f"Invalid message ID range: {e}")

async def handle_single_message(message):
    global is_stopped
    # Fetch a single message based on the provided link
    try:
        parts = message.text.split("/")
        chat_id = parts[-2]  # Extract chat ID from URL
        msg_id = int(parts[-1])  # Extract message ID from URL
        
        await fetch_message(message, msg_id, chat_id)
    except Exception as e:
        await bot.send_message(message.chat.id, f"Error handling single message: {e}", reply_to_message_id=message.id)

async def fetch_message(message, msg_id, chat_id):
    global is_stopped
    # Logic to fetch and handle a specific message
    try:
        if is_stopped:
            return  # Exit if the stop flag is set

        msg = await bot.get_messages(chat_id, msg_id)  # Use the bot client for fetching messages
        
        # Check if the message contains text or media
        if msg.text:
            await bot.send_message(message.chat.id, msg.text, reply_to_message_id=message.id)
        elif msg.photo:
            await bot.send_photo(message.chat.id, msg.photo.file_id, reply_to_message_id=message.id)
        elif msg.video:
            await bot.send_video(message.chat.id, msg.video.file_id, reply_to_message_id=message.id)
        elif msg.document:
            await bot.send_document(message.chat.id, msg.document.file_id, reply_to_message_id=message.id)
        else:
            await bot.send_message(message.chat.id, "This message contains unsupported media.", reply_to_message_id=message.id)
    except Exception as e:
        await bot.send_message(message.chat.id, f"Error fetching message: {e}", reply_to_message_id=message.id)

# Run the bot
bot.run()
