FROM python:3.10-slim

WORKDIR /app

# Copy your app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Expose internal port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
