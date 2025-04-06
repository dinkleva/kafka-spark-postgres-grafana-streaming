# from confluent_kafka import Producer
# import json
# import time
# from datetime import datetime

# # Kafka broker details
# conf = {'bootstrap.servers': 'kafka:9092'}  # Use 'kafka' because it's the service name in Docker Compose

# producer = Producer(conf)

# def delivery_report(err, msg):
#     """ Callback for message delivery reports """
#     if err is not None:
#         print(f"Message delivery failed: {err}")
#     else:
#         print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# topic = "new_topic"

# while True:
#     # Generate structured message
#     message = {
#         "message": f"Kafka event at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
#         "timestamp": datetime.now().isoformat()
#     }

#     # Convert to JSON string
#     message_json = json.dumps(message)

#     # Produce message to Kafka
#     producer.produce(topic, message_json.encode('utf-8'), callback=delivery_report)
#     producer.flush()  # Ensure messages are sent
#     time.sleep(2)  # Produces a message every 2 seconds





import json
import time
import mysql.connector
from datetime import datetime
from decimal import Decimal
from kafka import KafkaProducer

# Kafka Configuration
KAFKA_BROKER = "kafka:9092"
TOPIC = "amazon_topic"

batch_size = 100
offset = 0


# Connect to MySQL
db = mysql.connector.connect(
    host="mysql_source",
    user="user",
    password="userpass",
    database="source_db"
)
cursor = db.cursor(dictionary=True)

cursor.execute("SELECT COUNT(*) as total FROM amazon_products")
total_rows = cursor.fetchone()['total']
def json_serializer(obj):
    """Custom serializer for JSON encoding."""
    if isinstance(obj, Decimal):
        return float(obj)  # Convert Decimal to float
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime to string
    raise TypeError(f"Type {type(obj)} not serializable")

# Use this serializer in your Kafka producer


# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v, default=json_serializer).encode('utf-8')
)

while offset < total_rows:
    query = f"SELECT * FROM amazon_products LIMIT {batch_size} OFFSET {offset}"
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        print(" No new data found in MySQL.")
        break

    for row in rows:
        print(f" Sending to Kafka: {row}")
        future = producer.send(TOPIC, value=row)
        result = future.get(timeout=10)  # Ensure message is sent
    
    print(f" Message sent: ")
    producer.flush()  # Ensure all messages are delivered
    offset += batch_size
    time.sleep(1)

cursor.close()
db.close()
# producer.flush()

# while True:
#     fetch_and_send()
#     time.sleep(10)  # Fetch new data every 10 seconds
