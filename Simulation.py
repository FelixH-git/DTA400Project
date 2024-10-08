import simpy
import random
class Person():
    """
    Fundamental object of the virus simulation
    """
    id: int = 0
    dead: bool = False
    infected: bool = False
    traveling: bool = False
    region: str = ""
    virus_progression: float = 0

    def die(self):
        self.dead = True

    def __str__(self):
        format = f"Person            | {self.id}\ndead              | {self.dead}\ninfected          | {self.infected}\ntraveling         | {self.traveling}\nregion            | {self.region}\nvirus progression | {self.virus_progression}\n"
        return format

class Virus_Simulation():
    """
    Simulates a bunch of people, If two people are in the same region they have a chance equal to
    the infection_rate/virus_progression to infect another person, if the virus progression is 100%
    they either die or are cured 
    """
    def __init__(self, env, infection_rate):
        self._total_infected = 0
        self._total_people = []

    def init_world(self, population, region):
        for person in range(population):
            new_person = Person()
            new_person.id = person
            new_person.region = "Trollhättan"
            self._total_people.append(new_person)

    def infect(self):
        """
        Infects a random person
        """
        random_person = random.randint(0, len(self._total_people)-1)
        print(random_person)
        self._total_people[random_person].infected = True
        self._total_people[random_person].virus_progression += 1        

    def progress_infection(self):
        """
        Some function to increase the virus progression over the simulation time
        """
        pass

    def spread(self):
        """
        Function to spread the virus over some simulated time
        """
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
        for Person in self._total_people:
            if Person.infected == True:
                print(Person)


    def print_people(self):
        for person in self._total_people:
            print(person)
if __name__ == "__main__":
    simulation = Virus_Simulation(None, 0.20)
    
    simulation.init_world(5, "Trollhättan")
    simulation.infect()

    simulation.print_people()


    #simulation.print_infected()