import mysql.connector

config = {
    'user': "root",
    'password': "Devesh@@123",
    'host': 'localhost',
    'database': 'test_db_2_1',
    'raise_on_warnings': True
}


def fetch_updated_data():
    cnx = mysql.connector.connect(**config)

    cursor = cnx.cursor()

    table_name = 'task_table_temp3_2_1_4'

    query = f'SELECT * FROM {table_name}'
    cursor.execute(query)
    result = cursor.fetchall()

    data = {}

    for row in result:
        key = row[1]
        values = list(row[2:])
        data[key] = values

    cursor.close()
    cnx.close()

    print("SQL DATA FETCHED")
    print(data)
    return data

