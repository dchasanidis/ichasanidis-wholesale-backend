# Use official Python image as the base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Install PostgreSQL development libraries (including pg_config)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your FastAPI application code into the container
COPY . .

# Expose the FastAPI app port (default is 8000)
EXPOSE 8000

# Command to run the FastAPI app using uvicorn
CMD ["python", "main.py"]
