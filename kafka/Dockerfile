FROM python:3.9

# Install netcat (nc) for wait-for-mysql.sh
RUN apt-get update && apt-get install -y netcat-openbsd

# Set working directory
WORKDIR /app

# Copy files into the container
COPY ./scripts ./scripts
COPY ./config ./config
COPY wait-for-mysql.sh .
COPY requirements.txt .

# Make wait script executable
RUN chmod +x wait-for-mysql.sh

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start by waiting for MySQL, then run the producer
CMD ["sh", "-c", "./wait-for-mysql.sh && python3 scripts/producer.py"]
