import simpy
import random

import simpy.resources
class Person():
    """
    Fundamental object of the virus simulation
    """
    id: int = 0
    dead: bool = False
    infected: bool = False
    traveling: bool = False
    region: str = ""
    age: int = 25
    virus_progression: float = 0

    def increase_age(self):
        self.age += 1
    
    def travel(self):
        self.traveling = True
        
    def die(self):
        self.dead = True

    def __str__(self):
        format = f"Person            | {self.id}\nage               | {self.age}\ndead              | {self.dead}\ninfected          | {self.infected}\ntraveling         | {self.traveling}\nregion            | {self.region}\nvirus progression | {self.virus_progression}%\n"
        return format

class Virus_Simulation():
    """
    Simulates a bunch of people, If two people are in the same region they have a chance equal to
    the infection_rate/virus_progression to infect another person, if the virus progression is 100%
    they either die or are cured 
    """
    def __init__(self, env, infection_rate, num_hospistals):
        self._total_infected = 0
        self._infection_rate = infection_rate
        self.hospitals = simpy.Resource(env, num_hospistals)
        self._total_people = []
        self._region_separation = {}
    def init_world(self, population, regions:list):
        for person in range(population):
            new_person = Person()
            new_person.id = person
            new_person.region = random.choice(regions)
            new_person.age = random.randint(20,80)
            self._total_people.append(new_person)

        for _region in regions:
            self._region_separation.update({_region:[p for p in self._total_people if p.region == _region]})

    def infect(self):
        """
        Infects a random person
        """
        self._total_infected += 1
        random_person = random.randint(0, len(self._total_people)-1)
        print(random_person)
        self._total_people[random_person].infected = True
        #self._total_people[random_person].virus_progression += 1        

    def progress_infection(self, env, print_output=False):
        """
        Some function to increase the virus progression over the simulation time
        """
        for person in self._total_people:
            if person.infected:
                if print_output:
                    print(f"Virus progression increased on Person {person.id} on day {env.now:.2f} Virus progression is now at {person.virus_progression}.")
                person.virus_progression += 1 * person.age/10 + random.randint(1,100)/100
                yield env.timeout(1)
                

    def print_region(self, region):
        print(self._region_separation[region])
    
    def spread(self):
        """
        Function to spread the virus over some simulated time, for someone else to be infected they would need to be in the same region
        e.g. Two people in trollhättan can spread the infection to the other
        """
        for person in self._total_people:
            pass

    def intervention_method(self):
        """
        Some intervention method to reduce the spread of the virus e.g. reduce infenction rate
        """
        pass       

    def print_infected(self):
        """
        Prints Infected people
        """
        for person in self._total_people:
            if person.infected == True:
                print(person)

        print(f"\n----TOTAL INFECTED {self._total_infected}----")
    def print_people(self):
        for person in self._total_people:
            print(person)

def setup(env, num_hospitals, total_people):
    simulation = Virus_Simulation(env, 0.20, num_hospitals)

    simulation.init_world(total_people, ["Trollhättan", "Mellerud", "Vänersborg"])
    
    simulation.infect()
    simulation.print_region("Vänersborg")
    while(True):
        yield env.timeout(1)
        env.process(simulation.progress_infection(env, True))
        
    
if __name__ == "__main__":
    random.seed(42)
    env = simpy.Environment()
    env.process(setup(env, 1, 10))
    
    env.run(until=30)
    


    #simulation.print_infected()