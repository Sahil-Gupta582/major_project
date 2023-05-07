import mysql.connector

config = {
    'user': "",
    'password': "",
    'host': 'localhost',
    'database': 'test_db_2',
    'raise_on_warnings': True
}


def fetch_updated_data():
    cnx = mysql.connector.connect(**config)

    cursor = cnx.cursor()

    table_name = 'task_table'

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

