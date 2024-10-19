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

# Copy the start.sh script into the container
COPY start.sh .

# Make the start.sh script executable
RUN chmod +x start.sh

# Expose the port that your Flask app runs on (now 10000)
EXPOSE 10000

# Specify the command to run the start.sh script
CMD ["./start.sh"]
