FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Set environment variables (override with actual keys)
ENV GOOGLE_GENAI_API_KEY="AIzaSyAFtHcgwjrP6ltZEzKvTZeUnHCDRzOrXAM"
ENV TAVILY_API_KEY="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"
ENV FIRECRAWL_API_KEY="fc-278b83825f1749a3ba02f11815861fdc"
ENV GITHUB_TOKEN="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"

# Install cron and set up for 24/7 operation
RUN apt-get update && apt-get install -y cron

# Copy cron job
COPY cronjob /etc/cron.d/agent-cron
RUN chmod 0644 /etc/cron.d/agent-cron && crontab /etc/cron.d/agent-cron

# Create log directory
RUN mkdir -p /app/logs

# Start cron and keep container running
CMD ["sh", "-c", "cron && tail -f /dev/null"]