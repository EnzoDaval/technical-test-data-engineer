# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Change the working directory to src/moovitamix_fastapi
WORKDIR /app/src/moovitamix_fastapi

# Combine the script execution and the server start into one command
# CMD python -u /app/script.py && python -m uvicorn main:app --host 0.0.0.0 --port 8000
CMD python -m uvicorn main:app --host 0.0.0.0 --port 8000
