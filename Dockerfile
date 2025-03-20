FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    software-properties-common \
    postgresql postgresql-contrib \
    redis-server \
    openjdk-11-jdk wget curl \
    build-essential libssl-dev libffi-dev \
    && apt-get clean

RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt-get install -y \
    python3.8 python3.8-venv python3.8-dev python3.8-distutils \
    && apt-get clean

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.8

RUN pip install -r --no-cache-dir requirements.txt

WORKDIR /opt
RUN wget https://archive.apache.org/dist/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz && \
    tar -xvzf spark-3.5.5-bin-hadoop3.tgz && \
    mv spark-3.5.5-bin-hadoop3 spark && \
    rm spark-3.5.5-bin-hadoop3.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH="$SPARK_HOME/bin:$PATH"
ENV PYSPARK_PYTHON=python3

WORKDIR /workspace
COPY . /workspace/

RUN service postgresql start && \
    su - postgres -c "psql -c \"ALTER USER postgres PASSWORD 'postgres';\""

RUN sed -i 's/^supervised no/supervised systemd/' /etc/redis/redis.conf

EXPOSE 8888 5432 6379 8080

CMD service postgresql start && \
    service redis-server start && \
    jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.open_browser=False /workspace/main.ipynb
