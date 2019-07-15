from brains import Brain
from lib.sensors import GoalSensor
import random


class GeneticBrain(Brain):
    def __init__(self):
        self.angles = [15, 0, 0, 0, -15]
        self._fitness = None
        self.script = []
        self._script_i = 0
        self._parent_script_i = 0

    @classmethod
    def random(cls):
        b = GeneticBrain()
        b.script = []
        for i in range(0, 300):
            b.script += [random.choice(b.angles)] 
        return b
    
    def clone(self):
        c = GeneticBrain()
        c.script = list(self.script)
        return c

    def setup(self):                   
        self._fitness = None
        self.car.accelerate(10)
        self._script_i = 0
        self._parent_script_i = 0

    def update(self):
        if len(self.script) > 0: 
            script_command = self.script[self._script_i]
            self._script_i += 1        
            self.car.turn(script_command) 
    
    def mutate(self):
        for i in range(self._parent_script_i, len(self.script)):
            # if random.choice(range(0,1000)) > 800:
            self.script[i] = random.choice(self.angles)

    def fitness(self):
        if self._fitness is None:
            # create sensor here to improve performance
            s = GoalSensor(self.car)
            s.update()
            self._fitness = s.distance
        
        return self._fitness
