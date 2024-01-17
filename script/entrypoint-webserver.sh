#!/bin/bash
set -e
$(command -v pip) install "apache-airflow==2.8.0" "kafka-python==2.0.2"

#if [ -e "opt/airflow/requirements/requirements.txt" ]; then
#  $(command -v pip) install --user -r requirements/requirements.txt
#fi

if [ ! -f "opt/airflow/airflow.db" ]; then
  airflow db init && \
  airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin
fi

$(command -v airflow) db upgrade

exec airflow webserver