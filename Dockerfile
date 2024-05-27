# Use an official Python runtime as a parent image
FROM python:3.11.9-slim

# Create non root user
RUN useradd --create-home --shell /bin/bash app_user

# Set the working directory to /app
WORKDIR /home/app_user

# Copy the current directory contents into the container at /app
COPY http_benchmark.py /home/app_user
COPY requirements.txt  /home/app_user

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose ports 80 and 443 for HTTP and HTTPS connections, respectively
EXPOSE 80 443

# Change user role
USER app_user

# Run http_benchmark.py -u fireworks.ai -q 500 -t 10 -d 2 when the container launches
CMD ["python", "http_benchmark.py", "-u", "fireworks.ai", "-q", "500", "-t", "10", "-d", "2"]