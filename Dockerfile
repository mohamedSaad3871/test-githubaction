# Use official Python image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the app port (change if needed)
EXPOSE 3000

# Start the application
CMD ["python", "app.py"]
