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