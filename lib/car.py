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

    def __lt__(self, other):
        return self.totalReward > other.reward

    def __init__(self, track, brain, level, color="red"):
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
        self.totalReward = 0.0
        self.reward = 0.0
        self.level = level
        self.middlePoints = [
            # level 1
            [(100,535), (100,100),(700,100), (700,500), (200, 500)],
            # level 2
            [(72,503), (82,98), (662,86), (653,237), (368,233), (358,336), (643,343), (636,464), (203,488), (205,191)],
            # level 3
            [(461,127), (286,301), (461,408), (723,143), (424,18), (84,295), (486,562)],
            # level 4
            [(24,372), (129,252), (220,165), (272,148), (321,148), (386,195), (429,270), (446,337), (481,391), (532,405), (604,377), (646,337), (679,279), (747,215)],
            # Level 5
            [(166,447), (136,387), (136,330), (148,266), (180,226), (223,196), (285,171), (352,141), (436,136), (510,144), (561,178), (602,222), (623,278), (626,325), (620,377), (586,415), (526,451), (446,467), (360,477)],
            # Level 6
            [(152,448), (144,295), (166,177), (236,125), (342,97), (505,89), (629,97), (704,193), (700,337), (692,420), (629,500), (548,549), (415,550), (296,551), (253,485), (252,414), (268,338), (296,250), (370,217), (428,202), (520,202), (577,220), (605,269), (587,341), (548,398), (486,421), (384,405)]
        ]
        self.nextMiddlePoint = self.middlePoints[self.level-1][0]
        self.nextMiddlePointIndex = 0



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
        self.reward = 0
        '''Update the car status (brain, sensors, position, speed, direction, ...).'''
        if self.isalive:            
            self.brain.update()
            self.totalReward = self.totalReward - 0.01
            self.reward -= 0.01

            self.speed = self.speed + self.acceleration
            self.direction = (self.direction + self.steeringwheel) % 360 

            relativeposition = Point(0, self.speed).rotate(self.direction)
            self.position = self.position.move(relativeposition.x, -relativeposition.y)

            for s in self.sensors:
                s.update()

            self.distanceToCheckpoint = sqrt((self.position.x-self.nextMiddlePoint[0])*(self.position.x-self.nextMiddlePoint[0]) +
                    (self.position.y-self.nextMiddlePoint[1])*(self.position.y-self.nextMiddlePoint[1]))
            if self.distanceToCheckpoint  < 100 and self.nextMiddlePointIndex < len(self.middlePoints[self.level -1]):
                self.nextMiddlePoint = self.middlePoints[self.level-1][self.nextMiddlePointIndex]
                self.nextMiddlePointIndex = self.nextMiddlePointIndex + 1
                self.totalReward = self.totalReward + 0.3
                self.reward = self.reward + 0.3

            # check position
            if any([not self.track.intrack(*p) for p in self.points()]):        
                #print("!!!!!!!!!!!!!OUT OF TRACK!!!!!!!!!!!!!")
                self.totalReward = self.totalReward - 1
                self.reward = self.reward - 1
                self.isalive = False
                self.canvas.itemconfig(self.canvas_shape_id, fill="black")
            elif self.track.ingoal(*self.position):
                #print("!!!!!!!!!!!!! WON !!!!!!!!!!!!!")
                self.totalReward = self.totalReward + 1
                self.reward = self.reward + 1
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

