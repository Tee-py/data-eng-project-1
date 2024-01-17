#!/bin/bash
set -e
$(command -v pip) install "apache-airflow==2.8.0" "kafka-python==2.0.2"

#if [ -e "opt/airflow/requirements/requirements.txt" ]; then
#  $(command -v pip) install --user -r requirements/requirements.txt
#fi

$(command -v airflow) db upgrade

exec airflow scheduler