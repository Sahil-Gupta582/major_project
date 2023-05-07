import time

from populate_sql_data import populate_sql

from fetch_sql_data import fetch_updated_data

from prremptive_framework import task_framework

num_processors=4

while True:

    populate_sql()

    updated_data=fetch_updated_data()

    task_framework(updated_data,num_processors)

    time.sleep(20)




