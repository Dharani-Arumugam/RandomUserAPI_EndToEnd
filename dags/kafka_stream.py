# import uuid
# import json
# import logging
# import requests
# from datetime import datetime
#
# from airflow import DAG
# from airflow.providers.standard.operators.python import PythonOperator
# from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
# from airflow.providers.apache.kafka.hooks.produce import KafkaProducerHook
#
# default_args = {
#     'owner': 'dharani',
#     'start_date': datetime(2023, 11, 11, 11, 0),
# }
#
# def get_data():
#     """Fetch random user from API."""
#     response = requests.get('https://randomuser.me/api/').json()
#     return response['results'][0]
#
# def format_data(result):
#     """Format user data to a dict."""
#     location = result['location']
#     data = {
#         'id': str(uuid.uuid4()),
#         'first_name': result['name']['first'],
#         'gender': result['gender'],
#         'address': f"{location['street']['number']} {location['street']['name']}, "
#                    f"{location['city']}, {location['state']}, {location['country']}",
#         'post_code': location['postcode'],
#         'email': result['email'],
#         'user_name': result['login']['username'],
#         'dob': result['dob']['date'],
#         'registered_date': result['registered']['date'],
#         'phone': result['phone'],
#         'picture': result['picture']['medium'],
#     }
#     return data
#
# def produce_messages():
#     """
#     This function will be passed into ProduceToTopicOperator.
#     It must return an iterable of (key, value) pairs for KafkaProduction.
#     """
#     hook = KafkaProducerHook(kafka_config_id='kafka_default')
#     producer = hook.get_producer()
#
#     messages = []
#     for _ in range(20):
#         try:
#             raw = get_data()
#             formatted = format_data(raw)
#             key = formatted['id'].encode('utf-8')
#             value = json.dumps(formatted).encode('utf-8')
#             messages.append((key, value))
#         except Exception as e:
#             logging.error(f"Error formatting message: {e}")
#
#     # Return the key/value pairs
#     return messages
#
# with DAG(
#     dag_id='user_automation_kafka_airflow',
#     default_args=default_args,
#     schedule='@daily',
#     catchup=False,
#     tags=['example']
# ) as dag:
#
#     produce_task = ProduceToTopicOperator(
#         task_id='produce_users_to_kafka',
#         topic='users_created',
#         producer_function=produce_messages,
#         kafka_config_id='kafka_default',
#         synchronous=True,
#         poll_timeout=1.0,
#     )
#
#
#

###########################Sethupona code ################



import uuid
import json
import logging
import requests
from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from kafka import KafkaProducer
import time

default_args = {
    'owner': 'dharani',
    'start_date': datetime(2023, 11, 11, 11, 0),
}

def get_data():
    """Fetch random user from API"""
    response = requests.get('https://randomuser.me/api/')
    response = response.json()
    result = response['results'][0]
    return result

def format_data(result):
    """Format user data"""
    data = {}
    data['id'] = str(uuid.uuid4())
    data['first_name'] = result['name']['first']
    data['gender'] = result['gender']
    location = result['location']
    data['address'] = f"{location['street']['number']} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = result['email']
    data['user_name'] = result['login']['username']
    data['dob'] = result['dob']['date']
    data['registered_date'] = result['registered']['date']
    data['phone'] = result['phone']
    data['picture'] = result['picture']['medium']
    return data

def stream_data_to_kafka():
    """Task that runs inside the operator only"""

    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)

    records = 20  # send 20 messages per task run

    for _ in range(records):
        try:
            raw = get_data()
            formatted = format_data(raw)
            producer.send(
                'users_created',
                json.dumps(formatted).encode('utf-8')
            )
        except Exception as e:
            logging.error(f"Kafka publish failed: {e}")

    producer.flush()

with DAG(
    dag_id='user_automation',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    tags=['example']
) as dag:

    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data_to_kafka
    )