# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Install necessary packages for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire bot code into the container
COPY . .

# Expose the port that your Flask app runs on (now 10000)
EXPOSE 10000

# Specify the command to run your app and bot
CMD gunicorn app:app --bind 0.0.0.0:10000 & python3 bot.py
