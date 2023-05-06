import random
import math

# Define the tasks to be scheduled
tasks = [
    {"task_name": "job1", "task_priority": 50, "task_duration": 2.5, "task_energy": 4, "task_depends_on": []},
    {"task_name": "job2", "task_priority": 70, "task_duration": 1.8, "task_energy": 3, "task_depends_on": [1]},
    {"task_name": "job3", "task_priority": 80, "task_duration": 1.0, "task_energy": 2, "task_depends_on": [0]},
    {"task_name": "job4", "task_priority": 60, "task_duration": 2.2, "task_energy": 4, "task_depends_on": [1]},
    {"task_name": "job5", "task_priority": 90, "task_duration": 0.8, "task_energy": 1, "task_depends_on": [2, 3]}
]

# Define the number of processors available
num_processors = 2

# Define the maximum number of iterations for the PSO algorithm
max_iterations = 100

# Define the size of the swarm
swarm_size = 10

# Define the acceleration constants for the PSO algorithm
C1 = 1.49618
C2 = 1.49618

# Define the maximum and minimum velocity and position values for the particles in the swarm
max_velocity = 1
min_velocity = -1
max_position = num_processors - 1
min_position = 0

# Define the global best position and score
global_best_position = [0] * len(tasks)
global_best_score = float('inf')

# Define the particle class
class Particle:
    def __init__(self):
        # Initialize the position and velocity of the particle
        self.position = [random.randint(min_position, max_position) for _ in range(len(tasks))]
        self.velocity = [random.uniform(min_velocity, max_velocity) for _ in range(len(tasks))]
        
        # Initialize the personal best position and score of the particle
        self.best_position = self.position.copy()
        self.best_score = float('inf')
        
    def update_score(self):
        # Declare global variables
        global global_best_position, global_best_score
        
        # Calculate the score of the particle based on the completion time and energy consumption of the schedule
        completion_times = [0] * num_processors
        energy_consumptions = [0] * num_processors
        
        for i, task in enumerate(tasks):
            processor = self.position[i]
            depends_on = task['task_depends_on']
            duration = task['task_duration']
            energy = task['task_energy']
            
            # Calculate the start time of the task based on its dependencies and the completion times of its dependent tasks
            start_time = max(completion_times[j] for j in depends_on) if depends_on else 0
            
            # Calculate the completion time and energy consumption of the task on the assigned processor
            completion_time = start_time + duration
            energy_consumption = energy / duration
            
            # Update the completion time and energy consumption of the assigned processor
            completion_times[processor] = completion_time
            energy_consumptions[processor] += energy_consumption
            
        # Calculate the makespan and total energy consumption of the schedule
        makespan = max(completion_times)
        total_energy_consumption = max(energy_consumptions)
        
        # Update the personal best position and score of the particle if necessary
        if makespan < self.best_score:
            self.best_position = self.position.copy()
            self.best_score = makespan
            
        # Update the global best position and score if necessary
        if makespan < global_best_score:
            global_best_position = self.position.copy()
            global_best_score = makespan


    def update_position(self):
        # Update the velocity of the particle
        for i in range(len(self.velocity)):
            r1 = random.random()
            r2 = random.random()
            cognitive_velocity = C1 * r1 * (self.best_position[i] - self.position[i])
            social_velocity = C2 * r2 * (global_best_position[i] - self.position[i])
            self.velocity[i] += cognitive_velocity + social_velocity
            
            # Enforce the maximum and minimum velocity values
            self.velocity[i] = max(min(self.velocity[i], max_velocity), min_velocity)
            
        # Update the position of the particle
        for i in range(len(self.position)):
            self.position[i] = int(round(self.position[i] + self.velocity[i]))
            
            # Enforce the maximum and minimum position values
            self.position[i] = max(min(self.position[i], max_position), min_position)

    def run(self):
        # Run the particle by updating its position and score for a fixed number of iterations
        for i in range(max_iterations):
            self.update_position()
            self.update_score()

# Define the PSO function
def pso():
# Initialize the swarm
    swarm = [Particle() for _ in range(swarm_size)]
# Run the PSO algorithm for a fixed number of iterations
    for i in range(max_iterations):
        for particle in swarm:
            particle.run()

# Return the best schedule found by the PSO algorithm
    best_schedule = []
    for i, processor in enumerate(global_best_position):
        task_name = tasks[i]['task_name']
        start_time = sum(tasks[j]['task_duration'] for j in tasks[i]['task_depends_on'] if j in best_schedule) if tasks[i]['task_depends_on'] else 0
        best_schedule.append({'task_name': task_name, 'processor': processor, 'start_time': start_time})
    return best_schedule

# Test the PSO function
best_schedule = pso()
print(best_schedule)
