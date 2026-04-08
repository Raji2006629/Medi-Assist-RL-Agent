# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY inference.py .

# Expose port for API
EXPOSE 7860

# Run FastAPI using uvicorn
CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "7860"]
