FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (will be overridden by $PORT in production)
EXPOSE 8000

# Start the application
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --loop asyncio
