# 📊 Real-Time Data Pipeline: MySQL → Kafka → Spark → PostgreSQL → Grafana

This project demonstrates a **real-time streaming pipeline** built using **Dockerized microservices**. It simulates a data engineering workflow where product data (`amazon_products`) is ingested from **MySQL**, sent to **Kafka**, processed by **Spark Streaming**, stored in **PostgreSQL**, and finally visualized in **Grafana**.

---

## 🔧 Tech Stack

- 🐬 **MySQL** (Source Database)
- 🦄 **Apache Kafka** (Streaming Platform)
- ⚡ **Apache Spark Streaming** (Real-Time Processing)
- 🐘 **PostgreSQL** (Sink Database)
- 📊 **Grafana** (Data Visualization)
- 🐳 **Docker & Docker Compose** (Containerized Architecture)
- 🐍 **Python** (Kafka Producer)

---

## 📁 Project Structure

mysql-kafka-spark-postgres-grafana
├── docker-compose.yml 
├── mysql
│ └── init.sql # Initializes MySQL with amazon_products data 
├── kafka_producer
│ └── kafka_producer.py # Python script to send MySQL data to Kafka 
├── spark
│ └── spark_streaming.py # Spark job to consume from Kafka and write to PostgreSQL 
├── grafana
│ └── dashboards/ # Optional custom dashboards └── README.md

---

## 🧠 Pipeline Flow

1. **MySQL Source**: Contains `amazon_products` table with initial product data.
2. **Kafka Producer**: Reads in batches from MySQL and pushes each row as a message to a Kafka topic `amazon_products`.
3. **Spark Streaming Job**: Listens to the Kafka topic, processes the records, and inserts them into the PostgreSQL table.
4. **PostgreSQL Sink**: Stores processed product data for downstream use.
5. **Grafana**: Connects to PostgreSQL to visualize product categories, pricing trends, etc.

---

## 🚀 How to Run

### Clone and Start the Stack
```bash
git clone https://github.com/dinkleva/kafka-spark-postgres-grafana-streaming.git
cd kafka-spark-postgres-grafana-streaming
docker-compose up --build -d

### Now Copy kafka-spark-streaming.py file to spark-master container ###
docker cp kafka-spark-streaming.py saprk-master:/opt/bitnami/spark/

### Then exec this command to start spark-streaming-job ###
docker exec -it spark-master spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 /opt/bitnami/spark/kafka-spark-streaming.py

### This above command will insert the data to Postgres sql and then we can connect to postgres and visualize the data insights ###
📈 Grafana Dashboard Setup
Open Grafana at: http://localhost:3000

Login:

Username: admin

Password: admin

Add PostgreSQL as a Data Source:

Host: postgres:5432

Database: streaming_db

User: postgres

Password: postgres

Create a dashboard using the table amazon_products from PostgreSQL.

Make sure to select a numeric field for graphs.

Also add a time field (e.g. NOW() or a timestamp column if available).

🧪 Sample Table: amazon_products
id	title	price	category
1	Wireless Mouse	25.99	Electronics
2	Bluetooth Headphones	45.50	Audio

📌 Tips
Add a timestamp column in PostgreSQL for Grafana time series graphs.

Use producer.flush() in each batch loop to ensure Kafka delivery.

Ensure Spark can resolve the Kafka and Postgres container hostnames.

✅ Status
 MySQL initialized with mock data

 Kafka producer working

 Spark consumes from Kafka

 PostgreSQL receives processed data

 Grafana displays dynamic data

🤝 Contributions
Feel free to fork and enhance this project! Add alerts, schemas, or extend it with real-time dashboards and anomaly detection.

📜 License
MIT License. Use freely and responsibly.

Author