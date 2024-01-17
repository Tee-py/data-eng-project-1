from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'teepy',
    'start_date': datetime(2024, 1, 14, 13, 00)
}


def get_user_data():
    import requests

    response = requests.get("https://randomuser.me/api/")
    user_data = response.json()['results'][0]
    return user_data


def format_data(user_data):
    data = {}
    location = user_data['location']
    data['first_name'] = user_data['name']['first']
    data['last_name'] = user_data['name']['last']
    data['gender'] = user_data['gender']
    data['address'] = (f"{str(location['street']['number'])} {location['street']['name']} "
                       f"{location['city']} {location['state']} {location['country']}")
    data['postal_code'] = location['postcode']
    data['email'] = user_data['email']
    data['username'] = user_data['login']['username']
    data['dob'] = user_data['dob']['date']
    data['registered_date'] = user_data['registered']['date']
    data['phone'] = user_data['phone']
    data['picture'] = user_data['picture']['medium']
    return data


def stream_data():
    from kafka import KafkaProducer
    import time
    import json
    import logging

    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    curr_time = time.time()

    while True:
        if time.time() > curr_time + 60:
            break
        try:
            res = get_user_data()
            res = format_data(res)

            producer.send('users_created', json.dumps(res).encode('utf-8'))
        except Exception as e:
            logging.error(f"An Error occurred: {e}")
            continue


with DAG('user_automation', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )
