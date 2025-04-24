#!/bin/sh

echo "Waiting for MySQL to be ready..."

while ! nc -z mysql-source 3306; do
  sleep 1
done

echo "MySQL is up — executing Kafka producer..."

exec "$@"
