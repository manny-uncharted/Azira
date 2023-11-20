# Use the official Python 3.10 slim image
FROM python:alpine

WORKDIR /app

COPY . .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

EXPOSE 5556

# Install the required Python packages from requirements.txt
RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/python3 -m pip install --upgrade pip
RUN cat requirements.txt | while read package; do /opt/venv/bin/python -m pip install $package; done

# Using the script as the entrypoint
ENTRYPOINT ["sh", "./entrypoint.sh"]