import random
import math

# Define constants
NUM_DRONES = 5
NUM_TASKS = 10
MAX_ENERGY = 100
MAX_SPEED = 10
MAX_ITERATIONS = 100
C1 = 2
C2 = 2
W = 0.7

class Drone:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.energy = energy
        self.remaining_energy = energy
        self.best_position = (x, y)
        self.best_fitness = float('inf')
        
    def evaluate_fitness(self):
        return math.sqrt((self.x-self.best_position[0])**2 + (self.y-self.best_position[1])**2)
        
    def update_position(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        
    def update_best_position(self):
        if self.evaluate_fitness() < self.best_fitness:
            self.best_position = (self.x, self.y)
            self.best_fitness = self.evaluate_fitness()

# Initialize drones and global best position
swarm = [Drone(random.uniform(0, 100), random.uniform(0, 100), random.uniform(0, MAX_ENERGY)) for i in range(NUM_DRONES)]
global_best_position = (float('inf'), float('inf'))

# Define PSO functions
def update_swarm(global_best_position):
    for drone in swarm:
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)
        
        cognitive_velocity_x = C1 * r1 * (drone.best_position[0] - drone.x)
        cognitive_velocity_y = C1 * r1 * (drone.best_position[1] - drone.y)
        social_velocity_x = C2 * r2 * (global_best_position[0] - drone.x)
        social_velocity_y = C2 * r2 * (global_best_position[1] - drone.y)
        
        drone.velocity_x = W * drone.velocity_x + cognitive_velocity_x + social_velocity_x
        drone.velocity_y = W * drone.velocity_y + cognitive_velocity_y + social_velocity_y
        
        # Limit velocity to maximum speed
        speed = math.sqrt(drone.velocity_x**2 + drone.velocity_y**2)
        if speed > MAX_SPEED:
            drone.velocity_x = (drone.velocity_x / speed) * MAX_SPEED
            drone.velocity_y = (drone.velocity_y / speed) * MAX_SPEED
        
        drone.update_position()
        drone.update_best_position()

def get_global_best_position():
    global global_best_position
    for drone in swarm:
        if drone.evaluate_fitness() < math.sqrt((global_best_position[0])**2 + (global_best_position[1])**2):
            global_best_position = drone.best_position

# Run PSO algorithm
for i in range(MAX_ITERATIONS):
    get_global_best_position()
    update_swarm(global_best_position)

# Assign tasks to drones
tasks = [(random.uniform(0, 100), random.uniform(0, 100)) for i in range(NUM_TASKS)]
assigned_tasks = []

for i in range(len(tasks)):
    min_distance = float('inf')
    min_drone = None
    flag = -1
    for drone in swarm:
        distance = math.sqrt((tasks[i][0] - drone.x)**2 + (tasks[i][1] - drone.y)**2)
        if distance < min_distance and drone.remaining_energy >= distance:
            min_distance = distance
            min_drone = drone
            flag = 1
    if flag != -1:
        assigned_tasks.append((i+1, min_drone))
        min_drone.remaining_energy -= min_distance
    else:
        print("Task", i+1, "could not be scheduled")

# Print assigned tasks
for i in range(len(assigned_tasks)):
    print("Task", assigned_tasks[i][0], "assigned to drone at position", assigned_tasks[i][1].x, assigned_tasks[i][1].y, "with remaining energy", assigned_tasks[i][1].remaining_energy)
