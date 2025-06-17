FROM python:3.10-slim

# Install FFmpeg and Git
RUN apt-get update && apt-get install -y ffmpeg git && apt-get clean

# Set workdir
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run app
CMD ["python", "app.py"]
