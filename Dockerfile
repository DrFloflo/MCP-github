# Use official Python image
FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose MCP default port
EXPOSE 6277

# Set environment to production
ENV PYTHONUNBUFFERED=1

# Entry point to run the MCP server
CMD ["python", "server.py"]