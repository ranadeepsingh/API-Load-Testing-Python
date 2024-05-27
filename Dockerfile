# Use an official Python runtime as a parent image
FROM python:3.11.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY http_benchmark.py /app/
COPY requirements.txt  /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose ports 80 and 443 for HTTP and HTTPS connections, respectively
EXPOSE 80 443

# Run app.py when the container launches
CMD ["python", "http_benchmark.py"]