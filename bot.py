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

# Global variable to track ongoing downloads
ongoing_tasks = {}

async def download_file(url, chat_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                # Get the content type
                content_type = response.headers.get("Content-Type", "")
                
                if "video" in content_type or "application" in content_type:
                    filename = url.split("/")[-1]
                    async with aiofiles.open(filename, "wb") as f:
                        await f.write(await response.read())
                    return filename
            return None

async def fetch_video_url(page_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(page_url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                # Try to find the direct video URL
                video_tag = soup.find("video")
                if video_tag:
                    source = video_tag.find("source")
                    if source:
                        return source['src']  # return the video URL
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

    # Keep track of the ongoing task
    task = asyncio.create_task(process_upload(url, message.chat.id))
    ongoing_tasks[message.chat.id] = task  # Save the ongoing task

async def process_upload(url, chat_id):
    if url.startswith("http"):
        # Attempt to fetch the direct video URL first
        video_url = await fetch_video_url(url)

        if video_url:
            await message.reply("Downloading video...")
            filename = await download_file(video_url, chat_id)
            if filename:
                await bot.send_document(chat_id, filename)
                os.remove(filename)
                await bot.send_message(chat_id, "Video uploaded successfully.")
            else:
                await bot.send_message(chat_id, "Failed to download the video. Please check the URL.")
        else:
            # If we can't find a video, try to fetch links from the webpage
            links = await fetch_links(url)
            if links:
                await bot.send_message(chat_id, "Found links on the page:")
                for link in links:
                    await bot.send_message(chat_id, link)
            else:
                await bot.send_message(chat_id, "Failed to fetch links. Please check the URL.")
    else:
        await bot.send_message(chat_id, "Invalid URL. Please provide a direct file link or a valid website.")

@bot.on_message(filters.command("stop"))
async def stop_process(client, message):
    if message.chat.id in ongoing_tasks:
        ongoing_tasks[message.chat.id].cancel()  # Cancel the ongoing task
        await message.reply("Stopping the current process...")
        del ongoing_tasks[message.chat.id]  # Remove the task from tracking
    else:
        await message.reply("No ongoing process to stop.")

# Run the bot
bot.run()
