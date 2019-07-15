from brains import Brain
from lib.sensors import Sensor
import random


class ScriptedBrainForLevelOne(Brain):
    def setup(self): 
        self.script = []
        self.script += [(10, 0)]  # drive forward
        self.script += [(0,0)]*40 # wait
        self.script += [(-10, 0)] # stop
        self.script += [(10, 90)] # drive forward & turn right
        self.script += [(0,0)]*60 # wait
        self.script += [(-10, 0)] # stop
        self.script += [(10, 90)] # drive forward & turn right
        self.script += [(0,0)]*40 # wait
        self.script += [(-10, 0)] # stop
        self.script += [(10, 90)] # drive forward & turn right
        self.script += [(0,0)]*60 # wait
    
    def update(self):
        if len(self.script) > 0: 
            script_command = self.script.pop(0) # get first command
            self.car.accelerate(script_command[0])
            self.car.turn(script_command[1])            


class RandomDecisionsBrainForLevelOne(Brain):
    def setup(self):
        self.actions = []
        self.actions += [(2, 0)]   # drive forward
        self.actions += [(0,0)]    # wait
        self.actions += [(-2, 0)]  # drive backwards / stop
        self.actions += [(0, 90)]  # turn right
        self.actions += [(0, -90)] # turn left
    
    def update(self):
        script_command = random.choice(self.actions)
        self.car.accelerate(script_command[0])
        self.car.turn(script_command[1])     


class RuleBasedBrainForLevelOne(Brain):
    def setup(self):        
        self.front_center_sensor = Sensor(self.car, angle=0, x=0, y=15)
        
        # start driving
        self.car.accelerate(10)

    def update(self):
        if not self.front_center_sensor.is_obstacle_goal and self.front_center_sensor.distance < 20:
            self.car.turn(90)
