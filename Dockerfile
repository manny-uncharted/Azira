# Use the official Python 3.10 slim image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Update and upgrade the system packages
RUN apt update -y && \
    apt upgrade -y && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 5558
EXPOSE 5556


# Install the required Python packages from requirements.txt
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/python3 -m pip install --upgrade pip
RUN cat requirements.txt | while read package; do /opt/venv/bin/python -m pip install $package; done

# Command to run the Fastapi application
CMD [ "./entrypoint.sh" ]