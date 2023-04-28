import math
import random

# Constants
swarm_size = 20
max_iterations = 50
cognitive_parameter = 2.0
social_parameter = 2.0
inertia_weight = 0.7
drone_max_energy = 1000
drone_energy_rate = [2, 2.5, 1.5, 1.8, 2.2]
task_positions = [(34.0522, -118.2437), (40.7128, -74.0060), (41.8781, -87.6298), (51.5074, -0.1278), (35.6895, 139.6917)]
tasks = [{'position': pos, 'cost': random.randint(1, 50)} for pos in task_positions]

class Particle:
    def __init__(self, position):
        self.position = position
        self.velocity = [0] * len(position)
        self.best_position = position
        self.best_fitness = float('inf')
        self.fitness = float('inf')

    def evaluate_fitness(self):
        drone_energy = drone_max_energy
        total_task_cost = 0
        for i in range(len(self.position)):
            task_pos = tasks[i]['position']
            task_cost = tasks[i]['cost']
            dist = math.sqrt((task_pos[0] - self.position[i][0]) ** 2 + (task_pos[1] - self.position[i][1]) ** 2)
            time = dist / drone_energy_rate[i]
            drone_energy -= time * task_cost
            total_task_cost += task_cost

        self.fitness = total_task_cost
        if self.fitness < self.best_fitness:
            self.best_position = self.position
            self.best_fitness = self.fitness

class Swarm:
    def __init__(self, particle_class, swarm_size, max_iterations):
        self.particles = [particle_class([self.random_position() for _ in range(len(tasks))]) for _ in range(swarm_size)]
        self.best_particle = self.particles[0]
        self.max_iterations = max_iterations
        self.current_iteration = 0

    def random_position(self):
        return random.choice(task_positions)

    def run(self):
        while self.current_iteration < self.max_iterations:
            for particle in self.particles:
                particle.evaluate_fitness()
                if particle.fitness < self.best_particle.best_fitness:
                    self.best_particle = particle

            for particle in self.particles:
                for i in range(len(tasks)):
                    r1 = random.random()
                    r2 = random.random()
                    cognitive = cognitive_parameter * r1 * (particle.best_position[i][0] - particle.position[i][0],
                                                             particle.best_position[i][1] - particle.position[i][1])
                    social = social_parameter * r2 * (self.best_particle.best_position[i][0] - particle.position[i][0],
                                                       self.best_particle.best_position[i][1] - particle.position[i][1])
                    particle.velocity[i] = inertia_weight * particle.velocity[i] + cognitive + social
                    particle.position[i] = (particle.position[i][0] + particle.velocity[i][0], particle.position[i][1] + particle.velocity[i][1])

            self.current_iteration += 1

swarm = Swarm(Particle, swarm_size, max_iterations)
swarm.run()

# Print the best particle's position and fitness
print("Best Particle Position: {}".format(swarm.best_particle.best_position))
print("Best Particle Fitness: {}".format(swarm.best_particle.best_fitness))
