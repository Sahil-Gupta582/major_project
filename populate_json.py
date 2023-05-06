import json
import time
import random

task_id = 1

while True:
    data = {f'job{task_id}': [round(random.uniform(0.1, 2.9), 1), round(random.uniform(0.1, 5), 1), min(task_id - 1, random.randint(0, 3))]}
    filename = "new_tasks.json"

    try:
    	with open(filename,'r') as file:
    		existing_data=json.load(file)
    except FileNotFoundError:
    	existing_data={}

    existing_data.update(data)

    with open(filename, 'w') as file:
        json.dump(existing_data, file)

    print(f"Data appended to {filename}")

    task_id += 1

    time.sleep(5)
