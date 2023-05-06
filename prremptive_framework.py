import heapq
import time
import random

import random
import numpy as np

class Particle:
    def __init__(self, dim, bounds):
        self.position = np.random.uniform(bounds[0], bounds[1], size=dim).astype(np.float64)
        self.velocity = np.zeros(dim).astype(np.float64)
        self.best_position = np.zeros(dim).astype(np.float64)
        self.best_fitness = np.inf

class PSO:
    def __init__(self, num_particles, dim, bounds):
        self.num_particles = num_particles
        self.particles = [Particle(dim, bounds) for _ in range(num_particles)]
        self.global_best_position = np.zeros(dim).astype(np.float64)
        self.global_best_fitness = np.inf

    def run(self, max_iter):
        for _ in range(max_iter):
            for particle in self.particles:
                # update velocity
                r1 = np.random.rand(dim).astype(np.float64)
                r2 = np.random.rand(dim).astype(np.float64)
                cognitive_component = 2.0 * r1 * (particle.best_position - particle.position)
                social_component = 2.0 * r2 * (self.global_best_position - particle.position)
                particle.velocity += cognitive_component + social_component

                # update position
                particle.position += particle.velocity

                # evaluate fitness
                fitness = self.evaluate_fitness(particle.position)

                # update personal best
                if fitness < particle.best_fitness:
                    particle.best_position = particle.position.copy()
                    particle.best_fitness = fitness

                # update global best
                if fitness < self.global_best_fitness:
                    self.global_best_position = particle.position.copy()
                    self.global_best_fitness = fitness

    def evaluate_fitness(self, position):
        # calculate fitness
        return np.sum(position ** 2)        
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

        if self.energy != other.energy:
            return self.energy < other.energy
        else:
            return self.duration < other.duration 

    @staticmethod
    def minimum_completion_time():
        ready = [job for job in Job.jobs_dict.values() if not job.depends_on]
        current_time = 0
        while ready:
            job = min(ready)
            ready.remove(job)
            job.start_time = current_time
            current_time += job.duration
            job.finished = True
            print(f"Executing task {job.name} with duration {job.duration} and energy {job.energy}")
            for other_job in Job.jobs_dict.values():
                if job.name in other_job.depends_on:
                    other_job.depends_on.remove(job.name)
                    if not other_job.depends_on:
                        ready.append(other_job)
        print(f"Total completion time: {current_time+10}")

class GA_Scheduler:
    def __init__(self, jobs_dict, population_size=100, mutation_rate=0.1):
        self.jobs_dict = jobs_dict
        self.population_size = population_size
        self.mutation_rate = mutation_rate

    def generate_population(self):
        population = []
        for _ in range(self.population_size):
            job_names = list(self.jobs_dict.keys())
            random.shuffle(job_names)
            population.append(job_names)
        return population

    def evaluate_fitness(self, chromosome):
        tasks = [self.jobs_dict[job_name] for job_name in chromosome]
        time = 0
        energy = 0
        for task in tasks:
            if not task.depends_on or all(dep in chromosome for dep in task.depends_on):
                task.start_time = time
                time += task.duration
                energy += task.energy
                task.finished = True
                print(f"Executing task {task.name} with duration {task.duration} and energy {task.energy}")
            else:
                task.start_time = None
                task.finished = False
        print(f"Total completion time: {time}, Total energy: {energy}\n")
        return (time + energy)/2

    def selection(self, population):
        fitness_scores = [self.evaluate_fitness(chromosome) for chromosome in population]
        total_fitness = sum(fitness_scores)
        probabilities = [score / total_fitness for score in fitness_scores]
        parents = random.choices(population, weights=probabilities, k=2)
        return parents

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
        child2 = parent2[:crossover_point] + [gene for gene in parent1 if gene not in parent2[:crossover_point]]
        return child1, child2

    def mutation(self, chromosome):
        mutated_chromosome = chromosome.copy()
        for i in range(len(chromosome)):
            if random.random() < self.mutation_rate:
                j = random.randint(0, len(chromosome) - 1)
                mutated_chromosome[i], mutated_chromosome[j] = mutated_chromosome[j], mutated_chromosome[i]
        return mutated_chromosome

    def evolve(self, num_generations):
        population = self.generate_population()
        for _ in range(num_generations):
            parents = self.selection(population)
            children = self.crossover(parents[0], parents[1])
            mutated_children = [self.mutation(child) for child in children]
            population += mutated_children
            population = sorted(population, key=self.evaluate_fitness)[:self.population_size]
        best_chromosome = population[0]
        return [self.jobs_dict[job_name] for job_name in best_chromosome]


class MCT_Scheduler:
    def __init__(self):
        self.job_queue = []
        self.dependent_jobs = []
        self.running_job = None
        self.current_time = 0
        self.current_energy = 10

    def add_job(self, job):
        heapq.heappush(self.job_queue, job)

    def add_dependent_jobs(self, job):
        for dependent_job in self.job_queue:
            if dependent_job.depends_on == job.name:
                self.dependent_jobs.append(dependent_job)

    def run(self):
        while self.job_queue:
            highest_priority_job = heapq.nsmallest(len(self.job_queue), self.job_queue)[0]
            heapq.heappop(self.job_queue)

            self.add_dependent_jobs(highest_priority_job)

            if not self.dependent_jobs:
                if self.running_job is not None:
                    print(f"Interrupting job '{self.running_job.name}' with priority {self.running_job.priority} and duration {self.running_job.duration}...")
                    heapq.heappush(self.job_queue, self.running_job)
                self.running_job = highest_priority_job

                if highest_priority_job.duration > self.current_energy:
                    print(f"Not enough energy to run job '{highest_priority_job.name}'. Waiting for energy...")
                    energy_needed = highest_priority_job.duration - self.current_energy
                    self.current_energy = 0
                    time.sleep(energy_needed)
                    self.current_energy = 10
                else:
                    print(f"Running job '{highest_priority_job.name}' with priority {highest_priority_job.priority} and duration {highest_priority_job.duration}...")
                    self.current_energy -= highest_priority_job.duration
                    time.sleep(highest_priority_job.duration)
                    print(f"Job '{highest_priority_job.name}' completed in {highest_priority_job.duration} seconds.")
                self.running_job = None
            else:
                print(f"Checking job '{highest_priority_job.name}' with priority {highest_priority_job.priority} and duration {highest_priority_job.duration}...")
                for dependent_job in self.dependent_jobs:
                    print(f"  Running dependent job '{dependent_job.name}' with priority {dependent_job.priority} and duration {dependent_job.duration}...")
                    if dependent_job.duration > self.current_energy:
                        print(f"Not enough energy to run job '{dependent_job.name}'. Waiting for energy...")
                        energy_needed = dependent_job.duration - self.current_energy
                        self.current_energy =time.sleep(energy_needed)
                        self.current_energy = 10
                    else:
                        print(f"Running dependent job '{dependent_job.name}' with priority {dependent_job.priority} and duration {dependent_job.duration}...")
                        self.current_energy -= dependent_job.duration
                        time.sleep(dependent_job.duration)
                        dependent_job.finished = True
                        print(f"Dependent job '{dependent_job.name}' completed in {dependent_job.duration} seconds.")
                self.dependent_jobs = []

        print("All jobs completed.")

if __name__ == '__main__':
    start_time=time.time()
    Job.jobs_dict = jobs_dict={
        'job1': Job('job1', 1, 1.2, 2),
        'job2': Job('job2', 2, 0.5, 4, {'job1'}),
        'job3': Job('job3', 3, 2.3, 3),
        'job4': Job('job4', 4, 3.5, 1, {'job1', 'job3'}),
        'job5': Job('job5', 5, 1.8, 1),
        'job6': Job('job6', 6, 2.9, 5, {'job5'}),
        'job7': Job('job7', 7, 0.9, 3),
        'job8': Job('job8', 8, 0.7, 2, {'job6', 'job7'}),
        'job9': Job('job9', 9, 3.9, 2),
        'job10': Job('job10', 10, 0.6, 3, {'job2', 'job4', 'job9'}),
        'job11': Job('job11', 11, 2.2, 2),
        'job12': Job('job12', 12, 1.5, 1, {'job11'}),
        'job13': Job('job13', 13, 3.2, 3),
        'job14': Job('job14', 14, 1.1, 1, {'job11', 'job13'}),
        'job15': Job('job15', 15, 1.6, 4, {'job8', 'job10', 'job14'})
    }

    # -------------------------
    # GA
    # -------------------------
    
    scheduler = GA_Scheduler(Job.jobs_dict)
    best_schedule = scheduler.evolve(10)

    end_time = time.time()
    print(f"\nBest Schedule: {[job.name for job in best_schedule]}")
    print(f"Total execution time: {end_time - start_time:.2f} seconds\n\n")

    #-------------------------
    #MCT
    #-------------------------
    Job.minimum_completion_time()
    print()

    #-------------------------
    #PSO
    #-------------------------
    # pso = PSO(num_particles=10, num_iterations=20, c1=2.0, c2=2.0, w=0.7)
    # start_time = time.time()
    # task_sequence = pso.run()
    # end_time = time.time()
    # print(f"Task sequence: {task_sequence}")
    # print(f"Time taken: {end_time - start_time:.4f} seconds")
