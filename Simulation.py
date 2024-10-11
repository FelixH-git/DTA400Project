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
        format = f"\nPerson            | {self.id}\nage               | {self.age}\ndead              | {self.dead}\ninfected          | {self.infected}\ntraveling         | {self.traveling}\nregion            | {self.region}\nvirus progression | {round(self.virus_progression,2)}%\n"
        return format

class Virus_Simulation():
    """
    Simulates a bunch of people, If two people are in the same region they have a chance equal to
    the infection_rate/virus_progression to infect another person, if the virus progression is 100%
    they either die or are cured 
    """
    def __init__(self, env, infection_rate, num_hospistals, virus_growth_multiplier):
        self._total_infected = 0
        self._infection_rate = infection_rate
        self.hospitals = simpy.Resource(env, num_hospistals)
        self._total_people = []
        self._region_separation = {}
        self._virus_growth = virus_growth_multiplier
    
    def init_world(self, population, regions:list):
        for person in range(population):
            new_person = Person()
            new_person.id = person
            new_person.region = random.choice(regions)
            new_person.age = random.randint(1,45) + random.randint(1,45)
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

    def progress_infection(self, env, print_output=False):
        """
        Some function to increase the virus progression over the simulation time
        """
        for person in self._total_people:
            if person.infected:
                yield env.timeout(1)
                
                if print_output:
                    print(f"Virus progression increased on Person {person.id} on day {env.now:.2f} Virus progression is now at {round(person.virus_progression, 2)}%.")
                person.virus_progression += (1 * person.age/10 + random.randint(1,100)/100) * self._virus_growth
                if person.virus_progression > 100:
                    person.virus_progression = 100

                

    def print_region(self, _region):
        for person in self._region_separation[_region]:
            print(person)
    
    def spread(self,env, person):
        """
        Function to spread the virus over some simulated time, for someone else to be infected they would need to be in the same region
        e.g. Two people in trollhättan can spread the infection to the other
        """
        #We check if the person is in the same region, a prerequistie for spreading
        while self._total_infected < len(self._total_people):
            yield env.timeout(1)
            victim = random.choice(self._region_separation[person.region])
            
            if person != victim and not victim.infected:
                #We choose a random person from the same region and try to infect
                print(f"Person {person.id} Walks by person {victim.id} on day {env.now:.2f} and has a {self._infection_rate*100}% to infect victim")
                if random.random() < self._infection_rate:
                    print(f"Person {person.id} infects {victim.id}")
                    victim.infected = True
                    if len([p for p in self.get_region(person.region) if p.infected == True]) > len(self.get_region(person.region)):
                        self._total_infected = len(self.get_region(person.region))
                    self._total_infected += 1
                    #yield env.timeout(1)
                else:
                    print(f"Person {person.id} fails to infect victim {victim.id}")
                print(victim, "\n--Victim--\n", person, "\n--Infected perpetrator--\n")
                
                

    def intervention_method(self):
        """
        Some intervention method to reduce the spread of the virus e.g. reduce infenction rate
        """
        pass       

    def print_infected(self):
        """
        Prints Infected people
        """
        print("--------------------------")
        for person in self._total_people:
            if person.infected == True:
                print(person)

        print(f"\n----TOTAL INFECTED {self._total_infected}----")
    
    def print_total_infected(self):
        """
        Prints the number of total infected people
        """
        print(f"\n----TOTAL INFECTED {self._total_infected}----")
    def write_log_file(self):
        pass

    def get_infected(self):
        """
        Returns Infected people
        """
        return [p for p in self._total_people if p.infected == True]

    def get_region(self, region):
        return [p for p in self._total_people if p.region == region]

    def print_people(self):
        for person in self._total_people:
            print(person)

def setup(env, num_hospitals, total_people):
    
    simulation = Virus_Simulation(env, 0.70, num_hospitals, 0.5)

    simulation.init_world(total_people, ["Trollhättan", "Mellerud", "Vänersborg"])
    
    simulation.infect()
    
    simulation.print_infected()

    while(True):
        yield env.timeout(1)
        infected_people = simulation.get_infected()

        #random_person = random.randint(0, len([p for p in simulation._total_people if p.infected == True])-1)
        env.process(simulation.spread(env, random.choice(infected_people)))
        simulation.print_total_infected()
        print(f"TOTAL PEOPLE IN REGION {len(simulation.get_region("Vänersborg"))}")

        #env.process(simulation.progress_infection(env, True))
        
    
if __name__ == "__main__":
    random.seed(42)
    env = simpy.Environment()
    env.process(setup(env, 1, 100))
    env.run(until=30)
    

