import heapq
import time
import random

import heapq
import random
import numpy as np
import copy


class Processor:
    def __init__(self, name):
        self.name = name
        self.current_time = 0
        self.energy = float('inf')
        self.energy_consumption = 0

class Job:
    jobs_dict = {}

    def __init__(self, name, priority, duration, energy, depends_on=None):
        self.name = name
        self.priority = priority
        self.duration = duration
        self.energy = energy
        self.depends_on = depends_on or set()
        self.start_time = None
        self.finished = False
        Job.jobs_dict[name] = self

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.name < other.name
        return self.priority > other.priority

    @staticmethod
    def detect_cycle(job, visited, stack):
        visited.add(job)
        stack.add(job)

        for dependency in job.depends_on:
            if dependency not in Job.jobs_dict:
                continue  # Skip if the dependency doesn't exist
            if dependency not in visited:
                if Job.detect_cycle(Job.jobs_dict[dependency], visited, stack):
                    return True
            elif dependency in stack:
                return True

        stack.remove(job)
        return False

    @staticmethod
    def minimum_completion_time(num_processors=1):
        ready = [job for job in Job.jobs_dict.values() if not job.depends_on]
        heapq.heapify(ready)
        processors = [Processor(f'Processor {i+1}') for i in range(num_processors)]

        while ready or any(job.finished is False for job in Job.jobs_dict.values()):
            # Find available processors with enough energy to execute the task
            available_processors = [processor for processor in processors if processor.current_time < processor.energy]
            if not available_processors:
                break  # No available processors with enough energy

            # Assign tasks to available processors
            for processor in available_processors:
                if ready:
                    job = heapq.heappop(ready)
                    if not any(job.name == task.name and task.finished for task in Job.jobs_dict.values()):
                        if processor.current_time + job.duration <= processor.energy:
                            job.start_time = processor.current_time
                            processor.current_time += job.duration
                            processor.energy_consumption += job.energy
                            job.finished = True
                            print(f"Task {job.name} assigned to {processor.name}")

            # Update dependencies and add newly available tasks
            for job in Job.jobs_dict.values():
                if not job.finished:
                    dependent_tasks = {task for task in Job.jobs_dict.values() if job.name in task.depends_on}
                    if all(task.finished and not any(task.name == assigned_job.name for assigned_job in ready) for task in dependent_tasks):
                        job.depends_on = set()
                        heapq.heappush(ready, job)

        total_time = max(processor.current_time for processor in processors)
        total_energy_consumption = sum(processor.energy_consumption for processor in processors)
        print(f"Total completion time: {total_time}")
        print(f"Total energy consumption: {total_energy_consumption}")
        return total_time,total_energy_consumption


    @staticmethod
    def remove_deadlocks():
        visited = set()
        stack = set()

        for job in Job.jobs_dict.values():
            if job not in visited:
                if Job.detect_cycle(job, visited, stack):
                    print(f"Deadlock detected involving job: {job.name}")
                    # Handle deadlock here (e.g., remove the job or break the dependency)

    @staticmethod
    def assign_tasks_pso(num_processors=1, num_particles=10, num_iterations=100, inertia=0.5, c1=1, c2=2):
        # Initialize particles
        particles = []
        for _ in range(num_particles):
            particle = Particle(num_processors)
            particles.append(particle)

        global_best_fitness = float('inf')
        global_best_positions = []

        for _ in range(num_iterations):
            for particle in particles:
                # Update particle's position and velocity
                particle.update_velocity(inertia, c1, c2, global_best_positions)
                particle.update_position()

                # Evaluate fitness
                fitness = particle.calculate_fitness()
                if fitness < global_best_fitness:
                    global_best_fitness = fitness
                    global_best_positions = copy.deepcopy(particle.positions)

        # Assign tasks based on global best positions
        processors = [Processor(f'Processor {i+1}') for i in range(num_processors)]
        for i, job_name in enumerate(Job.jobs_dict.keys()):
            processor_index = global_best_positions[i]
            processor = processors[processor_index]
            job = Job.jobs_dict[job_name]
            job.start_time = processor.current_time
            processor.current_time += job.duration
            processor.energy_consumption += job.energy
            job.finished = True
            print(f"Task {job.name} assigned to {processor.name}")

        total_time = max(processor.current_time for processor in processors)
        total_energy_consumption = sum(processor.energy_consumption for processor in processors)
        print(f"Total completion time: {total_time}")
        print(f"Total energy consumption: {total_energy_consumption}")
        return total_time,total_energy_consumption


    @staticmethod
    def assign_tasks_ga(num_processors=1, population_size=50, num_generations=100, tournament_size=5, mutation_rate=0.1):
        # Initialize population
        population = []
        for _ in range(population_size):
            individual = Individual(num_processors)
            population.append(individual)

        for generation in range(num_generations):
            # Evaluate fitness for each individual in the population
            for individual in population:
                individual.calculate_fitness()

            # Sort the population based on fitness in ascending order
            population.sort(key=lambda x: x.fitness)

            # Select parents for the next generation using tournament selection
            parents = []
            for _ in range(population_size):
                tournament = random.sample(population, tournament_size)
                winner = min(tournament, key=lambda x: x.fitness)
                parents.append(winner)

            # Create the next generation through crossover and mutation
            next_generation = []
            for i in range(population_size):
                parent1 = parents[i]
                parent2 = random.choice(parents)
                child = parent1.crossover(parent2)
                child.mutate(mutation_rate)
                next_generation.append(child)

            population = next_generation

        # Assign tasks based on the best individual in the final population
        best_individual = min(population, key=lambda x: x.fitness)
        processors = [Processor(f'Processor {i+1}') for i in range(num_processors)]
        for i, job_name in enumerate(Job.jobs_dict.keys()):
            processor_index = best_individual.sequence[i]
            processor = processors[processor_index]
            job = Job.jobs_dict[job_name]
            job.start_time = processor.current_time
            processor.current_time += job.duration
            processor.energy_consumption += job.energy
            job.finished = True
            print(f"Task {job.name} assigned to {processor.name}")

        total_time = max(processor.current_time for processor in processors)
        total_energy_consumption = sum(processor.energy_consumption for processor in processors)
        print(f"Total completion time: {total_time}")
        print(f"Total energy consumption: {total_energy_consumption}")
        return total_time,total_energy_consumption

class Particle:
    def __init__(self, num_processors):
        self.num_processors = num_processors
        self.positions = []
        self.velocities = []
        self.best_positions = []
        self.best_fitness = float('inf')

        for _ in range(len(Job.jobs_dict)):
            position = random.randint(0, num_processors - 1)
            velocity = random.uniform(-1, 1)
            self.positions.append(position)
            self.velocities.append(velocity)
            self.best_positions.append(position)

    def update_velocity(self, inertia, c1, c2, global_best_positions):
        if len(self.positions) < len(global_best_positions):
            last_position = self.positions[-1]
            self.positions.extend([last_position] * (len(global_best_positions) - len(self.positions)))

        for i in range(len(global_best_positions)):
            r1 = random.uniform(0, 1)
            r2 = random.uniform(0, 1)
            inertia_term = inertia * self.velocities[i]
            cognitive_component = c1 * r1 * (self.best_positions[i] - self.positions[i])
            social_component = c2 * r2 * (global_best_positions[i] - self.positions[i])
            self.velocities[i] = inertia_term + cognitive_component + social_component


    def update_position(self):
        for i in range(len(Job.jobs_dict)):
            self.positions[i] = int(round(self.positions[i] + self.velocities[i]))

            # Clamp position within the valid range
            if self.positions[i] < 0:
                self.positions[i] = 0
            elif self.positions[i] >= self.num_processors:
                self.positions[i] = self.num_processors - 1

    def calculate_fitness(self):
        processors = [Processor(f'Processor {i+1}') for i in range(self.num_processors)]

        for i, job_name in enumerate(Job.jobs_dict.keys()):
            processor_index = self.positions[i]
            processor = processors[processor_index]
            job = Job.jobs_dict[job_name]
            job.start_time = processor.current_time
            processor.current_time += job.duration
            processor.energy_consumption += job.energy

        total_time = max(processor.current_time for processor in processors)
        total_energy_consumption = sum(processor.energy_consumption for processor in processors)
        fitness = total_time + total_energy_consumption

        if fitness < self.best_fitness:
            self.best_fitness = fitness
            self.best_positions = copy.deepcopy(self.positions)

        return fitness

class Individual:
    def __init__(self, num_processors):
        self.num_processors = num_processors
        self.sequence = []
        self.fitness = float('inf')

        for _ in range(len(Job.jobs_dict)):
            position = random.randint(0, num_processors - 1)
            self.sequence.append(position)

    def crossover(self, other):
        child = Individual(self.num_processors)
        crossover_point = random.randint(0, len(self.sequence) - 1)
        child.sequence = self.sequence[:crossover_point] + other.sequence[crossover_point:]
        return child

    def mutate(self, mutation_rate):
        for i in range(len(self.sequence)):
            if random.uniform(0, 1) < mutation_rate:
                self.sequence[i] = random.randint(0, self.num_processors - 1)

    def calculate_fitness(self):
        processors = [Processor(f'Processor {i+1}') for i in range(self.num_processors)]

        for i, job_name in enumerate(Job.jobs_dict.keys()):
            processor_index = self.sequence[i]
            processor = processors[processor_index]
            job = Job.jobs_dict[job_name]
            job.start_time = processor.current_time
            processor.current_time += job.duration
            processor.energy_consumption += job.energy

        total_time = max(processor.current_time for processor in processors)
        total_energy_consumption = sum(processor.energy_consumption for processor in processors)
        self.fitness = total_time + total_energy_consumption


def task_framework(ref_dict,num_processors):

    jobs_dict={}

    for idx,val in enumerate(ref_dict.items()):
        name=list(val)[0]
        duration=list(val)[1][0]
        energy=list(val)[1][1]
        dependencies=list(val)[1][2]
        jobs_dict[name] = Job(name, idx, duration, energy, dependencies)

    num_tasks=len(ref_dict)

    Job.jobs_dict=jobs_dict
    
    # Remove deadlocks
    Job.remove_deadlocks()

    # -------------------------
    # MCT
    # -------------------------

    # Calculate minimum completion time
    mct_time,mct_energy=Job.minimum_completion_time(num_processors)
    print()
    print()

    # -------------------------
    # GA
    # -------------------------

    # Assign tasks using Genetic Algorithm
    population_size = 50  # Number of individuals in the population
    num_generations = 100  # Number of generations for GA
    tournament_size = 5  # Tournament size for parent selection
    mutation_rate = 0.1  # Probability of mutation

    ga_time,ga_energy=Job.assign_tasks_ga(num_processors, population_size, num_generations, tournament_size, mutation_rate)
    print()
    print()


    #-------------------------
    #PSO
    #-------------------------

    # Assign tasks using Particle Swarm Optimization
    num_particles = 10  # Number of particles in the swarm
    num_iterations = 100  # Number of iterations for PSO
    inertia = 0.5  # Inertia weight
    c1 = 1  # Cognitive component weight
    c2 = 2  # Social component weight

    pso_time,pso_energy=Job.assign_tasks_pso(num_processors, num_particles, num_iterations, inertia, c1, c2)

    #-------------------------
    #SUMMARY 
    #-------------------------

    summary_table = f'''
    +-------------------+---------------------+-------------------------+
    |  Number of        |                     {num_processors:<19}       |
    |  Processors       |                                               |                         
    +-------------------+---------------------+-------------------------+
    |  Number of        |                    {num_tasks:<19}        |                         
    |  Tasks            |                                               |                         
    +-------------------+---------------------+-------------------------+
    |   Algorithm       |  Final Completion   |   Total Energy Needed   |
    |                   |        Time         |                         |
    +-------------------+---------------------+-------------------------+
    |      PSO          |   {pso_time:<18.2f}|    {pso_energy:<19.2f}  |
    +-------------------+---------------------+-------------------------+
    |      GA           |   {ga_time:<18.2f}|    {ga_energy:<19.2f}  |
    +-------------------+---------------------+-------------------------+
    |      MCT          |   {mct_time:<18.2f}|    {mct_energy:<19.2f}  |
    +-------------------+---------------------+-------------------------+
    '''


    print(summary_table)



if __name__ == '__main__':
    # Create job dictionary

    jobs_dict = {}

    num_tasks=10

    for i in range(1, num_tasks+1):
        name = f'job{i}'
        duration = round(random.uniform(0.1, 2.9), 1)
        energy = round(random.uniform(0.1, 5), 1)
        dependencies_count = min(i - 1, random.randint(0, 3))
        dependencies = set(random.sample(range(1, i), dependencies_count))

        jobs_dict[name] = Job(name, i, duration, energy, dependencies)
        print(name, i, duration, energy, dependencies)
        print()


    num_processors = 4  # Number of processors to assign tasks to
    Job.jobs_dict = jobs_dict

    # Remove deadlocks
    Job.remove_deadlocks()

    # -------------------------
    # MCT
    # -------------------------

    # Calculate minimum completion time
    mct_time,mct_energy=Job.minimum_completion_time(num_processors)
    print()
    print()

    # -------------------------
    # GA
    # -------------------------

    # Assign tasks using Genetic Algorithm
    population_size = 50  # Number of individuals in the population
    num_generations = 100  # Number of generations for GA
    tournament_size = 5  # Tournament size for parent selection
    mutation_rate = 0.1  # Probability of mutation

    ga_time,ga_energy=Job.assign_tasks_ga(num_processors, population_size, num_generations, tournament_size, mutation_rate)
    print()
    print()


    #-------------------------
    #PSO
    #-------------------------

    # Assign tasks using Particle Swarm Optimization
    num_particles = 10  # Number of particles in the swarm
    num_iterations = 100  # Number of iterations for PSO
    inertia = 0.5  # Inertia weight
    c1 = 1  # Cognitive component weight
    c2 = 2  # Social component weight

    pso_time,pso_energy=Job.assign_tasks_pso(num_processors, num_particles, num_iterations, inertia, c1, c2)

    #-------------------------
    #SUMMARY 
    #-------------------------

    summary_table = f'''
    +-------------------+---------------------+-------------------------+
    |  Number of        |                     {num_processors:<19}       |
    |  Processors       |                                               |                         
    +-------------------+---------------------+-------------------------+
    |  Number of        |                    {num_tasks:<19}        |                         
    |  Tasks            |                                               |                         
    +-------------------+---------------------+-------------------------+
    |   Algorithm       |  Final Completion   |   Total Energy Needed   |
    |                   |        Time         |                         |
    +-------------------+---------------------+-------------------------+
    |      PSO          |   {pso_time:<18.2f}|    {pso_energy:<19.2f}  |
    +-------------------+---------------------+-------------------------+
    |      GA           |   {ga_time:<18.2f}|    {ga_energy:<19.2f}  |
    +-------------------+---------------------+-------------------------+
    |      MCT          |   {mct_time:<18.2f}|    {mct_energy:<19.2f}  |
    +-------------------+---------------------+-------------------------+
    '''


    print(summary_table)
