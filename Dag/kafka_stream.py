from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import json
import requests



default_args = {
    "owner":"airscholar",
    "start_date":datetime(2024, 3, 8, 10, 00)

}

def get_data():
    response = requests.get('https://randomuser.me/api/')
    response = response.json()
    res = response['results'][0]
    # print(json.dumps(res, indent=3))
    return res
def format_data(res):
    data = {}
    location = res["location"]
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['lgender'] = res['gender']
    data['address'] =f'{str(location["street"]["number"])} {location["street"]["name"]} \
        {location["city"]} {location["state"]} {location["country"]}'
    data["post_code"] = {location["postcode"]}
    data["email"] = res["email"]
    data["username"] = res["login"]["username"]
    data["dob"] = res["dob"]["date"]
    data["registered_date"] =res["registered"]["date"]
    data["phone"] = res["phone"]
    data["picture"] = res['picture']['medium']

    return data


def stream_data():
    data = get_data()
    format_out = format_data(data)
    print(format_out)


# stream_data()

# with DAG("user_automation",
#          default_args=default_args,
#          catchup=False) as dag:
#     streaming_task = PythonOperator(
#         task_id = 'stream_data_from_api',
#         python_callable=stream_data
#     )

if __name__ =="__main__":
    stream_data()
    