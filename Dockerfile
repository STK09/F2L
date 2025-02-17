# Use the official Python image as a base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files to the container
COPY . .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose any necessary ports (if applicable)
EXPOSE 8080

# Command to run the bot
CMD ["python", "bot.py"]
