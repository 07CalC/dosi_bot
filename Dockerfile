# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY dosi.py .
COPY dosi_beta.py .

# Set environment variable for bot token
ENV BOT_TOKEN=""

# Run the bot (using dosi.py as default, change to dosi_beta.py if needed)
CMD ["python", "-u", "dosi.py"]
