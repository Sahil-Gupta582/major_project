import heapq
import time
import random

import random
import numpy as np

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
