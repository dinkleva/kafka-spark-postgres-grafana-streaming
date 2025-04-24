import time
import mysql.connector
import json
from kafka import KafkaProducer
from producer_utils import json_serializer, load_config

# loading configuration
config = load_config("config/producer-config.yml")

KAFKA_BROKER = config['kafka']['broker']
TOPIC = config['kafka']['topic']
BATCH_SIZE = config['mysql']['batch_size']
TABLE = config['mysql']['table']

#connecting to mysql
db = mysql.connector.connect(
    host=config['mysql']['host'],
    user=config['mysql']['user'],
    password=config['mysql']['password'],
    database=config['mysql']['database']

)

# setting cursor to database
cursor = db.cursor(dictionary=True)
cursor.execute(f"SELECT COUNT(*) as total FROM {TABLE}")
total_rows = cursor.fetchone()['total']


#kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v, default=json_serializer).encode('utf-8')
)

offset = 0

while offset < total_rows:
    query = f"SELECT * FROM {TABLE} LIMIT {BATCH_SIZE} OFFSET {offset}"
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        print("No new data found in mysql")
        break
    for row in rows:
        print(f"Sending to kafka: {row}")
        future = producer.send(TOPIC, value=row)
        future.get(timeout=10)
    
    producer.flush()
    offset += BATCH_SIZE
    time.sleep(2)

cursor.close()
db.close()