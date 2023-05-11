import json
import time
from decimal import Decimal

from fetch_sql_data import fetch_updated_data
from prremptive_framework import task_framework

num_processors = 4

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)  # Convert Decimal to string
        return super().default(o)

while True:
    updated_data = fetch_updated_data()
    run_data = task_framework(updated_data, num_processors)
    print('here', run_data)

    try:
        with open('simulation_output.json', 'r') as json_file:
            file_contents = json_file.read()
            existing_data = json.loads(file_contents) if file_contents else []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(run_data)

    with open('simulation_output.json', 'w') as json_file:
        json.dump(existing_data, json_file, cls=DecimalEncoder)

    time.sleep(20)
