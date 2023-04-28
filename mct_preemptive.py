import numpy as np

# Define the problem
def objective_function(completion_time):
    return completion_time

# Define the tasks and their processing times
tasks = np.array([1, 2, 3, 4])
processing_times = np.array([5, 3, 4, 2])

# Initialize the scheduling system
current_time = 0
scheduled_tasks = []

# Repeat until all tasks are completed
while len(scheduled_tasks) < len(tasks):
    remaining_processing_times = processing_times - (current_time - scheduled_tasks)
    available_tasks = np.where(remaining_processing_times > 0)[0]
    next_task = available_tasks[np.argmin(remaining_processing_times[available_tasks])]
    scheduled_tasks.append(current_time)
    current_time += processing_times[next_task]

# Evaluate the solution
completion_time = scheduled_tasks[-1] + processing_times[next_task]
objective_value = objective_function(completion_time)
print(f"Completion time: {completion_time}, Objective value: {objective_value}")
