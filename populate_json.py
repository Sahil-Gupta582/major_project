import json
import time
import random
import os

task_id = 1

filename = "new_tasks.json"

while True:
    dependencies_count = min(task_id - 1, random.randint(0, 3))
    dependencies = list(set(random.sample(range(1, task_id), dependencies_count)))

    if len(list(dependencies))==0:
    	dependencies=None

    data = {f'job{task_id}': [round(random.uniform(0.1, 2.9), 1), round(random.uniform(0.1, 5), 1), dependencies]}

    if os.path.isfile(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = {}

    existing_data.update(data)

    with open(filename, 'w') as file:
        json.dump(existing_data, file)

    print(f"Data appended to {filename}")

    task_id += 1

    time.sleep(3)
