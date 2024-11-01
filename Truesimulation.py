"""
Carwash example.

Covers:

- Waiting for other processes
- Resources: Resource

Scenario:
  A carwash has a limited number of washing machines and defines
  a washing processes that takes some (random) time.

  Car processes arrive at the carwash at a random time. If one washing
  machine is available, they start the washing process and wait for it
  to finish. If not, they wait until they can use one.

"""

import itertools
import random
import csv
import simpy
import statistics
import numpy as np

RANDOM_SEED = 42
NUM_BEDS = 50  # Number of machines in the carwash    # Minutes it takes to clean a car
T_INTER = 10       # 
SIM_TIME = T_INTER * 100    # Simulation time in minutes
VIRUS_SEVERITY = 1
QUE_LIMIT = 5
# fmt: on


class Hospital:
    """A Hospital has a limited number of bed (``NUM_BEDS``) to
    treat people in parallel.

    People have to request one of the beds. When they got one, they
    can start the treating processes and wait for it to finish.

    """

    def __init__(self, env, num_beds):
        self.env = env
        self.beds = simpy.Resource(env, num_beds)
        self.treat_time = []
        self.dead_people = 0
        self.person_request = {}
        self.service_rate = {}
        self.arrivals = 0
        self.amount_serviced = 0
        self.waiting_time = []
        self.server_utilization = {}
        self.servers_utilazed = 0
        self.que_length = {}
        
        
    def treat(self, person, symptom_severity , age):
        """The treating processes. It takes a ``person`` processes and tries
        to treat it."""
        treat_time = (age/10 * symptom_severity/10) * VIRUS_SEVERITY
        yield self.env.timeout(treat_time)
        self.amount_serviced += 1
        self.treat_time.append(treat_time)
        self.service_rate.update({self.env.now : self.amount_serviced})
        print(f"Hospital treats person {person}.")


def person(env, person, hospital : Hospital, symptom_severity, age):
    hospital.arrivals += 1
    if len(hospital.beds.queue) > QUE_LIMIT:
        hospital.beds.release(hospital.beds.queue[0])
        hospital.dead_people += 1

    arrive = env.now
    print(f'{person} who is age {age} and symptom severity is at {symptom_severity}% arrives at the hospital at {env.now:.2f}.')
    with hospital.beds.request() as request:
        result = yield request | env.timeout(arrive)
        hospital.server_utilization.update({round(env.now, 2) : hospital.beds.count/hospital.beds.capacity})
        hospital.que_length.update({round(env.now, 2) : round(len(hospital.beds.queue)/env.now,2) * 100})
        if request in result:
            hospital.person_request.update({person : request})
            print(f'{person} begins treatment at {env.now:.2f}.')
            yield env.process(hospital.treat(person, symptom_severity, age))
            print(f'{person} leaves the hospital at {env.now:.2f}.')
        else:
            waiting_time = env.now - arrive
            hospital.waiting_time.append(waiting_time/env.now)
            
def write_csv_file(data : dict | list, fields, filename):
    
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        if type(data) == dict:
            for key, value in data.items():
                writer.writerow([key,value])
        elif type(data) == list:
            for value in data:
                writer.writerow([value])    
def setup(env, num_beds, t_inter):

    # Create the carwashs
    hospital = Hospital(env, num_beds)

    person_count = itertools.count()
    
    avg_job_time = {}
    dead_people_dict = {}
    arrival_rate_dict = {}
    while True:
        yield env.timeout(random.choice(np.random.poisson(lam=2, size=500)))
        
        
        env.process(person(env, f'Person {next(person_count)}', hospital, random.randint(0, 100), (random.randint(0,45) + random.randint(0,45))))
        
        
        if len(hospital.treat_time) > 0:
            avg_job_time.update({env.now : sum(hospital.treat_time)/len(hospital.treat_time)})
            dead_people_dict.update({env.now : hospital.dead_people})
            arrival_rate_dict.update({env.now : round(hospital.arrivals/env.now, 2)})
            write_csv_file(arrival_rate_dict, ['hour', 'arrival_rate'], "arrival_rate.csv")
            write_csv_file(dead_people_dict, ['hour', 'amount_dead_people'], "dead_people.csv")
            write_csv_file(avg_job_time, ['hour', 'avg_job_time'], "Jobtime.csv")
            write_csv_file(hospital.service_rate, ['hour', 'amount_serviced'], 'service_rate.csv')
            write_csv_file(hospital.server_utilization, ['hour', "beds_utiliazed"], "Utilization.csv")
            write_csv_file(hospital.waiting_time, ['wait_time'], "wait_time.csv")
            write_csv_file(hospital.que_length, ['hour','que_length'], 'Que_length.csv')


random.seed(RANDOM_SEED)  # This helps to reproduce the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, 15, T_INTER))

# Execute!
env.run(until=SIM_TIME)