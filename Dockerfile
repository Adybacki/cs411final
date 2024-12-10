# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install SQLite3
RUN apt-get update && apt-get install -y sqlite3

# Copy the rest of the application code into the container
COPY . /app

# Define a volume for persisting the database
VOLUME ["/app/db"]

# Expose port 5000 to the world outside this container
EXPOSE 5000

# Run the entrypoint script when the container launches
CMD ["python", "app.py"]
