FROM postgres:latest
COPY init/ /docker-entrypoint-initdb.d/
ENV POSTGRES_DB=amazon
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postpass