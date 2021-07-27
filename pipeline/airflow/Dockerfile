FROM apache/airflow:2.1.2
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  && apt-get install curl wget \
  && pip install apache-airflow-providers-ftp \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
