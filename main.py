import json
import time

from fetch_sql_data import fetch_updated_data
from prremptive_framework import task_framework

num_processors = 16

while True:
    updated_data = fetch_updated_data()
    run_data = task_framework(updated_data, num_processors)
    print('here',run_data)

    try:
        with open('simulation_output.json', 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []

    existing_data.append(run_data)

    with open('simulation_output.json', 'w') as json_file:
        json.dump(existing_data, json_file)

    time.sleep(20)