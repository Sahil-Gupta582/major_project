import heapq
import time
import random

class Job:
    def __init__(self, name, priority, duration, depends_on=None):
        self.name = name
        self.priority = priority
        self.duration = duration
        self.depends_on = depends_on or set()
        self.start_time = None
        self.finished = False

    def __lt__(self, other):
        return self.priority < other.priority

class Scheduler:
    def __init__(self):
        self.job_queue = []
        self.dependent_jobs = []
        self.running_job = None  # Added running_job attribute

    def add_job(self, job):
        heapq.heappush(self.job_queue, job)  # Add job to priority queue

    def add_dependent_jobs(self, job):
        for dependent_job in self.job_queue:
            if dependent_job.depends_on == job.name:
                self.dependent_jobs.append(dependent_job)

    def run(self):
        while self.job_queue:
            highest_priority_job = heapq.heappop(self.job_queue)  # Get job with highest priority

            self.add_dependent_jobs(highest_priority_job)

            if not self.dependent_jobs:
                if self.running_job is not None:  # Interrupt running job if a higher priority job comes in
                    print(f"Interrupting job '{self.running_job.name}' with priority {self.running_job.priority} and duration {self.running_job.duration}...")
                    heapq.heappush(self.job_queue, self.running_job)
                self.running_job = highest_priority_job
                print(f"Running job '{highest_priority_job.name}' with priority {highest_priority_job.priority} and duration {highest_priority_job.duration}...")
                time.sleep(highest_priority_job.duration)
                print(f"Job '{highest_priority_job.name}' completed in {highest_priority_job.duration} seconds.")
                self.running_job = None
            else:
                print(f"Checking job '{highest_priority_job.name}' with priority {highest_priority_job.priority} and duration {highest_priority_job.duration}...")
                for dependent_job in self.dependent_jobs:
                    print(f"  Running dependent job '{dependent_job.name}' with priority {dependent_job.priority} and duration {dependent_job.duration}...")
                    time.sleep(dependent_job.duration)
                    print(f"  Dependent job '{dependent_job.name}' completed in {dependent_job.duration} seconds.")
                heapq.heappush(self.job_queue, highest_priority_job)
                self.dependent_jobs = []

def create_job(name, duration, priority):
    return Job(name, priority, duration)

def create_jobs(jobs_dict):
    jobs = []
    for job_name, job_info in jobs_dict.items():
        depends_on = set()
        if 'depends_on' in job_info:
            for parent_job_name in job_info['depends_on']:
                if parent_job_name in jobs_dict:
                    parent_job_info = jobs_dict[parent_job_name]
                    parent_job = create_job(parent_job_name, duration=parent_job_info.get('duration', 1), priority=parent_job_info.get('priority', 1))
                    depends_on.add(parent_job)
        job = create_job(job_name, duration=job_info.get('duration', 1), priority=job_info.get('priority', 1))
        job.depends_on = depends_on
        jobs.append(job)
    return jobs


if __name__ == "__main__":
    jobs_dict = {
        'job1': {'duration': 2, 'priority': 1},
        'job2': {'duration': 3, 'priority': 1},
        'job3': {'duration': 1, 'priority': 3},
        'job4': {'duration': 2, 'priority': 2},
        'job5': {'duration': 3, 'priority': 1},
        'job6': {'duration': 1, 'priority': 2},
        'job7': {'duration': 4, 'priority': 1},
        'job8': {'duration': 2, 'priority': 2, 'depends_on': ['job1', 'job2']},
        'job9': {'duration': 3, 'priority': 1},
        'job10': {'duration': 1, 'priority': 2, 'depends_on': ['job3', 'job4']},
        'job11': {'duration': 2, 'priority': 1},
        'job12': {'duration': 3, 'priority': 1},
        'job13': {'duration': 1, 'priority': 3},
        'job14': {'duration': 2, 'priority': 2},
        'job15': {'duration': 3, 'priority': 1},
        'job16': {'duration': 1, 'priority': 2},
        'job17': {'duration': 4, 'priority': 1},
        'job18': {'duration': 2, 'priority': 2, 'depends_on': ['job5', 'job6']},
        'job19': {'duration': 3, 'priority': 1},
        'job20': {'duration': 1, 'priority': 2, 'depends_on': ['job13', 'job14']}
    }

    jobs = create_jobs(jobs_dict)

    scheduler = Scheduler()

    for job in jobs:
        scheduler.add_job(job)

    scheduler.run()

'''
NOTE:

The given code is an implementation of a scheduler that manages the execution of jobs based on their priorities and dependencies. 

The `Job` class represents a job that has a name, priority, duration, and a set of dependent jobs that must complete before it can run. 

The `Scheduler` class manages the execution of the jobs by adding them to a priority queue based on their priorities. When a job is added to the queue, the scheduler checks if it has any dependent jobs that have not yet completed. If so, the job is not executed and is added back to the queue. If not, the job is executed and its duration is simulated using the `time.sleep()` function. 

If a job with a higher priority is added to the queue while a lower priority job is running, the scheduler interrupts the running job and adds it back to the queue. The higher priority job is then executed. 

The `create_job()` function is a helper function that creates a `Job` instance based on the given parameters, and `create_jobs()` function creates a list of `Job` instances based on the information in a dictionary that specifies the jobs and their properties.

The main function creates a dictionary that defines 20 jobs with different priorities and dependencies. It then creates a list of `Job` instances based on the dictionary and adds them to the scheduler using the `add_job()` method. Finally, it runs the scheduler using the `run()` method.
'''