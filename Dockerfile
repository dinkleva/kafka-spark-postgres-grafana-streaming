FROM python:3.9
WORKDIR /app
COPY kafka_producer.py requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install confluent-kafka
CMD ["python3", "kafka_producer.py"]
