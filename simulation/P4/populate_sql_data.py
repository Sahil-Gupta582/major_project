import json
import mysql.connector


config = {
    'user': "root",
    'password': "Devesh@@123",
    'host': 'localhost',
    'database': 'test_db_2_1'
}

def populate_sql():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_table_temp3_2_1_4 (
            task_id INT AUTO_INCREMENT PRIMARY KEY,
            task_name VARCHAR(255),
            completion_time FLOAT,
            energy_needed FLOAT,
            dependencies VARCHAR(255)
        )
    """)

    with open('new_tasks.json', 'r') as file:
        data = json.load(file)

    for task_name, task_data in data.items():
        completion_time, energy_needed, dependencies = task_data
        
        if dependencies is None:
            dependencies = None
        else:
            dependencies = json.dumps(dependencies)
        
        query = """
            INSERT INTO task_table_temp3_2_1_4 (task_name, completion_time, energy_needed, dependencies)
            VALUES (%s, %s, %s, %s)
        """
        values = (task_name, completion_time, energy_needed, dependencies)
        
        cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

    print("SQL DATA UPDATED\n")
