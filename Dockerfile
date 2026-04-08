FROM python:3.12-slim

WORKDIR /app

# Copy code
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for Gradio
EXPOSE 7860

# Launch app
CMD ["python", "app.py"]
