#
# CAR & BRAIN
#
# Contains the Car and Brain base class.
#
import tkinter
from math import cos, sin, pi, radians, sqrt
from lib.math2d import Point, Line, Vector
from lib.tracks import Track
from lib.sensors import Sensor

class Car:    
    '''A car.'''  
    _shape = [(-10,-15),(-10,15), (10,15), (10,-15)]
    
    def __init__(self, track, brain, color="red"):   
        self.canvas = track.canvas 
        self.canvas_shape_id = None    
        self.track = track
        self.position = Point(*track.startpoint)
        self.direction = track.startdirection
        self.steeringwheel = 0 # -90 ... left, 0 ... forward, 90 ... right
        self.acceleration = 0 # -10 ... slow down, 0 ... keep, 10 ... speed up
        self.speed = 0
        self.brain = brain        
        self.color = color
        self.isalive = True
        self.sensors = []
        self.brain.initialize(self)


    def points(self):        
        '''Points of the car shape.'''
        return [(self.position.x + x, self.position.y - y) for x,y in [Point(x,y).rotate(self.direction) for x,y in self._shape]]

    def accelerate(self, units):
        '''Accelerate the car about units.'''
        self.acceleration = max(-10, min(10, units))        

    def turn(self, units):     
        '''Turn the car about units to the left (negative) or right (positive).'''   
        self.steeringwheel = max(-90, min(90, units))

    def update(self):
        '''Update the car status (brain, sensors, position, speed, direction, ...).'''
        if self.isalive:            
            self.brain.update()

            # update speed and direction
            self.speed = self.speed + self.acceleration
            self.direction = (self.direction + self.steeringwheel) % 360 

            # update position
            relativeposition = Point(0, self.speed).rotate(self.direction)
            self.position = self.position.move(relativeposition.x, -relativeposition.y)
            
            # update sensor  
            for s in self.sensors:
                s.update()

            # check position
            if any([not self.track.intrack(*p) for p in self.points()]):        
                #print("!!!!!!!!!!!!!OUT OF TRACK!!!!!!!!!!!!!")
                self.isalive = False
                self.canvas.itemconfig(self.canvas_shape_id, fill="black")
            elif self.track.ingoal(*self.position):
                #print("!!!!!!!!!!!!! WON !!!!!!!!!!!!!")
                self.isalive = False
                self.canvas.itemconfig(self.canvas_shape_id, fill="blue")
            
            self.acceleration = 0        
            self.steeringwheel = 0

    def draw(self):
        '''Draw the car on the canvas.'''
        if self.canvas_shape_id is None:
            self.canvas_shape_id = self.canvas.create_polygon(*self.points(), fill=self.color)
        else:
            self.canvas.coords(self.canvas_shape_id, *[item for sublist in self.points() for item in sublist])
        
        for s in self.sensors:
            s.draw()

###############################################################################
# BRAIN
###############################################################################

class Brain:    
    '''Represents the brain of a car. Do not override this.'''
    def initialize(self,car):    
        '''Initialize the state of the brain.'''
        self.car = car
        self.track = car.track
        self.setup()
    def setup(self):
        '''Setup the brain.'''
        pass
    def update(self):
        '''Update the brain.'''
        pass

