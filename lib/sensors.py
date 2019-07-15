#
# SENSORS
#
# Contains the Sensor and GoalSensor classes.
#
from math import cos, sin, pi, radians, sqrt
from lib.math2d import Point, Line, Vector


class Sensor:    
    '''Sensor that measures the distance to the edge of roadway.'''

    # measured values    
    distance = 1000
    obstacle = None
    is_obstacle_goal = False

    def __init__(self, car, angle, x, y):
        # sensor itself
        self.direction_relative_to_car = angle
        self.position_relative_to_car = Point(x,y)
        self.direction = 0
        self.position = Point(0,0)
        self.sensor_line_id = None



        # connection to car
        self.car = car
        self.car.sensors.append(self)

    def update(self):        
        '''Update the position of the sensor and its measurements.'''     
        # update direction
        self.direction = self.car.direction + self.direction_relative_to_car

        # update position
        relativesensor = self.position_relative_to_car.rotate(self.car.direction)
        self.position = self.car.position.move(relativesensor.x, -relativesensor.y)        

        # update distance & obstacle
        relativeray = Point(0, 1000).rotate(self.direction)
        ray = self.position.move(relativeray.x, -relativeray.y)
        
        nearest_point_meassured = self.measure(self.car.track.shapes(), self.position, ray)
        if nearest_point_meassured is None:
            self.distance = 1000
            self.obstacle = None
        else:            
            self.obstacle, self.distance = nearest_point_meassured
            self.is_obstacle_goal = self.car.track.ingoal(*self.obstacle)
        
    def draw(self):     
        '''Draw the sensor.'''   
        if self.sensor_line_id is None:
            if self.obstacle is not None:
                self.sensor_line_id = self.car.canvas.create_line(*self.position, *self.obstacle, fill="orange", dash=(1,1))
        elif self.obstacle is not None:
            self.car.canvas.coords(self.sensor_line_id, *self.position, *self.obstacle)                
            self.car.canvas.itemconfig(self.sensor_line_id, fill="blue" if self.is_obstacle_goal else "orange")                    

    def measure(self, shapes, frompoint, topoint):
        '''Measure the distance from point frompoint to the first intersection of line (frompoint,topoint) with shapes.'''
        nearest_point = (None, None)
        for shape in shapes:
            points = self.car.track.intersections(shape, frompoint, topoint)        
            points = [(p,frompoint.distance(p)) for p in points if p is not None]        
            points.sort(key=lambda p: p[1]) # by distance
            if len(points) > 0:
                if nearest_point[1] is None or nearest_point[1] > points[0][1]:
                    nearest_point = points[0]
        return nearest_point if nearest_point[1] is not None else None

    def __repr__(self):
        return f"(sensor position on car: {self.position}, distance: {self.distance})"


class GoalSensor(Sensor):
    '''Sensor that measures distance remaining to drive to goal.'''
    def __init__(self, car):
        super(GoalSensor, self).__init__(car, 0, 0, 0)                
        self.obstacle = None
        self.is_obstacle_goal = True # set to always true
    
    def draw(self):
        '''Goal sensor is invisible.'''
        pass
    
    def update(self):
        '''Update measurement.'''
        self.distance = self.measure()

    def measure(self):   
        '''Measure distance to goal.'''
        x = self.car.position.x
        y = self.car.position.y     
        min_distance = 9999
        min_distance_point_on_midline = None
        min_distance_line_index = None

        midline_lines = [Line(Point(*self.car.track.midline_points[i]), Point(*self.car.track.midline_points[i+1])) for i in range(0, len(self.car.track.midline_points)-1)]

        for i in range(0, len(midline_lines)):            
            l = Line(Point(x,y), Point(x,y).move(*Vector.from_points(*midline_lines[i]).normal_vector()))
            s = midline_lines[i].intersection(l, treat_as_line_segments=False)
            if s is not None and midline_lines[i].inline(s):                
                d = Vector.from_points(Point(x,y), s).length()                    
                if min_distance > d:
                    min_distance = d
                    min_distance_point_on_midline = s
                    min_distance_line_index = i
            
            # if outside of line use distance to endpoints
            ad = Vector.from_points(midline_lines[i].a, Point(x,y)).length()
            bd = Vector.from_points(midline_lines[i].b, Point(x,y)).length()
            if min_distance > ad:
                min_distance = ad
                min_distance_point_on_midline = midline_lines[i].a
                min_distance_line_index = i                
            if min_distance > bd:
                min_distance = bd
                min_distance_point_on_midline = midline_lines[i].b
                min_distance_line_index = i                
        
        # sum up distances
        distance = Vector.from_points(min_distance_point_on_midline,midline_lines[min_distance_line_index].b).length()
        for i in range(min_distance_line_index+1, len(midline_lines)):
            distance = distance + midline_lines[i].length()        
        
        return distance - 25 # remove length of goal area
