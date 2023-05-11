import json
import time
import random
import os
import mysql.connector

task_id = 1

filename = "new_tasks.json"

config = {
    'user': "root",
    'password': "Devesh@@123",
    'host': 'localhost',
}

# Connect to MySQL server without specifying the database
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Create the database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS test_db_2_1")
cursor.execute("USE test_db_2_1")

# Create the table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_table_temp3_2_1_5 (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(255),
        completion_time DECIMAL(3, 1),
        energy_needed DECIMAL(3, 1),
        dependencies JSON
    )
""")

# Close the cursor and connection to apply changes
cursor.close()
conn.close()

while True:
    conn = mysql.connector.connect(**config, database='test_db_2_1')
    cursor = conn.cursor()

    dependencies_count = min(task_id - 1, random.randint(0, 3))
    dependencies = list(set(random.sample(range(1, task_id), dependencies_count)))

    if len(dependencies) == 0:
        dependencies = None

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

    query = """
        INSERT INTO task_table_temp3_2_1_5 (task_name, completion_time, energy_needed, dependencies)
        VALUES (%s, %s, %s, %s)
    """

    task_name = f'job{task_id}'
    completion_time, energy_needed, dependencies = data[task_name]

    if dependencies is None:
        dependencies = None
    else:
        dependencies = json.dumps(dependencies)

    values = (task_name, completion_time, energy_needed, dependencies)

    cursor.execute(query, values)
    task_id += 1

    conn.commit()

    cursor.close()
    conn.close()

    print("SQL DATA UPDATED\n")

    time.sleep(15)
