FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Environment variables will be set in Render dashboard for security
# DO NOT hardcode secrets here

# Install cron and set up for 24/7 operation
RUN apt-get update && apt-get install -y cron

# Copy cron job
COPY cronjob /etc/cron.d/agent-cron
RUN chmod 0644 /etc/cron.d/agent-cron && crontab /etc/cron.d/agent-cron

# Create log directory
RUN mkdir -p /app/logs

# Start cron and keep container running
CMD ["sh", "-c", "cron && tail -f /dev/null"]