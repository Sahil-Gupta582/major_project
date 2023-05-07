import time

from fetch_sql_data import fetch_updated_data

from prremptive_framework import task_framework

num_processors=4

while True:

    updated_data=fetch_updated_data()

    task_framework(updated_data,num_processors)

    time.sleep(20) 




