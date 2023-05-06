import heapq
import time
import random

import random
import numpy as np

from Genetic_Scheduler import GA_Scheduler

from MCT_Scheduler import MCT_Scheduler

from PSO_Scheduler import Particle,PSO
      
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

if __name__ == '__main__':
    start_time=time.time()
    
    #Static Sample
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
