FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Environment variables will be set in GitHub Secrets for security
# DO NOT hardcode secrets here

# Create log directory
RUN mkdir -p /app/logs

# Default command for GitHub Actions
CMD ["python", "main.py"]