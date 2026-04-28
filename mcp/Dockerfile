FROM python:3.10-slim

WORKDIR /app

# Install nginx + curl (for debugging)
RUN apt-get update && apt-get install -y nginx curl

COPY . .

RUN pip install --no-cache-dir fastmcp wikipedia requests

# Replace nginx config
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD service nginx start && python server.py
