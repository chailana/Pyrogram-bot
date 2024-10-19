#!/bin/bash

# Start the Flask app and the Pyrogram bot
gunicorn app:app & python3 bot.py
