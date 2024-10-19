import os
import pyrogram
from pyrogram import Client, filters
import aiohttp
from bs4 import BeautifulSoup
import asyncio

# Your bot token and credentials
bot_token = "7490926656:AAHG-oUUzGPony9xfyApSI0EbbymhneDU1k"
api_id = 22420997
api_hash = "d7fbe2036e9ed2a1468fad5a5584a255"

# Initialize the bot client
bot = Client("url_uploader_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

async def download_file(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content_type = response.headers.get("Content-Type", "")
                if "application" in content_type or "image" in content_type or "video" in content_type:
                    filename = url.split("/")[-1]
                    with open(filename, "wb") as f:
                        f.write(await response.read())
                    return filename
            return None

async def fetch_links(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                return [a['href'] for a in soup.find_all('a', href=True)]
            return []

@bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply("👋 Welcome to the URL Uploader Bot!\n"
                        "Send me a command like `/upload <url>` to upload files from a direct link or a website.")

@bot.on_message(filters.command("upload"))
async def upload_file(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide a URL to upload.")
        return

    url = message.command[1]
    await message.reply("Processing your request...")

    # Check if it's a direct file link or a website
    if url.startswith("http"):
        # Attempt to download the file
        filename = await download_file(url)

        if filename:
            await message.reply("Uploading file...")
            await bot.send_document(message.chat.id, filename)
            os.remove(filename)
            await message.reply("File uploaded successfully.")
        else:
            # If the download fails, try to fetch links from the webpage
            links = await fetch_links(url)
            if links:
                await message.reply("Found links on the page:")
                for link in links:
                    await bot.send_message(message.chat.id, link)
            else:
                await message.reply("Failed to download the file or fetch links. Please check the URL.")
    else:
        await message.reply("Invalid URL. Please provide a direct file link or a valid website.")

@bot.on_message(filters.command("stop"))
async def stop_process(client, message):
    await message.reply("Stopping the current process...")
    # Implement logic here to stop any ongoing process if needed.

# Run the bot
bot.run()
