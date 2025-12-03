#!/bin/bash
set -e

# Install Python dependencies if requirements.txt exists
if [ -f "/opt/airflow/requirements.txt" ]; then
  python -m pip install --upgrade pip
  pip install -r /opt/airflow/requirements.txt
fi

airflow db migrate
## Create first Airflow user if required
#if [[ "${_AIRFLOW_WWW_USER_CREATE}" == "true" ]]; then
#  echo "Creating Airflow admin user..."
#  airflow users create \
#    --username "${_AIRFLOW_WWW_USER_USERNAME}" \
#    --password "${_AIRFLOW_WWW_USER_PASSWORD}" \
#    --firstname "Airflow" \
#    --lastname "Admin" \
#    --role Admin \
#    --email "admin@example.com" || true
#fi

# Run the command passed in Docker Compose
exec "$@"