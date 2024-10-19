import os
import pyrogram
from pyrogram import Client, filters
import aiohttp
from bs4 import BeautifulSoup
import urllib.parse

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
                # If the URL is a direct file link
                if "application" in content_type or "image" in content_type or "video" in content_type:
                    filename = url.split("/")[-1]
                    with open(filename, "wb") as f:
                        f.write(await response.read())
                    return filename
                # If the URL is a webpage, extract downloadable links
                elif "text/html" in content_type:
                    return await extract_links_from_page(url)
            return None

async def extract_links_from_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                links = []
                # Find all links on the page
                for anchor in soup.find_all('a', href=True):
                    link = anchor['href']
                    # Validate and normalize the link
                    full_url = urllib.parse.urljoin(url, link)
                    links.append(full_url)
                
                return links
    return None

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
    await message.reply("Downloading file...")

    # Download the file
    result = await download_file(url)
    
    if isinstance(result, list):
        await message.reply("Found links on the page:\n" + "\n".join(result))
    elif result:
        await message.reply("Uploading file...")
        await bot.send_document(message.chat.id, result)
        os.remove(result)  # Clean up the file after uploading
        await message.reply("File uploaded successfully.")
    else:
        await message.reply("Failed to download the file. Please check the URL and ensure it's valid.")

@bot.on_message(filters.command("stop"))
async def stop_process(client, message):
    await message.reply("Stopping the current process...")
    # Implement logic here to stop any ongoing process if needed.

# Run the bot
bot.run()
