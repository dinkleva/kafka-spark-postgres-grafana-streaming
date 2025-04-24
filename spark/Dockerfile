FROM bitnami/spark:latest

USER root

RUN install_packages python3 python3-pip

RUN pip3 install --upgrade pip

RUN mkdir -p /opt/spark/jars

COPY . /opt/spark_app

RUN mkdir -p /opt/spark/jars

RUN pip3 install -r /opt/spark_app/requirements.txt

WORKDIR /opt/spark_app

ENV PYTHONPATH="/usr/local/lib/python3.10/dist-packages:$PYTHONPATH"

COPY ./jars/postgresql-42.3.3.jar /opt/spark/jars/

ENTRYPOINT [ "/opt/bitnami/spark/bin/spark-submit", "--master", "spark://spark-master:7077", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5", "/opt/spark_app/main.py" ]
