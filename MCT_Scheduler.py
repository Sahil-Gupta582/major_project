import heapq
import time
import random

import random
import numpy as np

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
