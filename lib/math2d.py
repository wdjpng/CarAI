#
# MATH CLASSES FOR 2D
#
# Contains classes and methods for calculations in the two dimensional world.
# 
from math import cos, sin, pi, radians, sqrt, acos, degrees


class Point:
    '''Represents a point.'''
    def __init__(self, x,y):
        self.x = x
        self.y = y
    
    def rotate(self, angle):
        '''Rotate this point around the z-axis.'''
        angle = radians(angle)
        return Point(self.x * cos(angle) + self.y * sin(angle), -self.x*sin(angle) + self.y*cos(angle))
    
    def distance(self, p2):
        '''Calculate the distance between this point and another point.'''
        p1 = self
        return sqrt( (p2.x-p1.x)**2 + (p2.y - p1.y)**2 )

    def move(self, dx, dy):        
        '''Return a point that is moved about dx and dy.'''
        return Point(self.x + dx, self.y + dy)

    def __iter__(self):
        return [self.x, self.y].__iter__()

    def __repr__(self):
        return str(self.x) + "," + str(self.y)
    
    def astuple(self):
        '''Return the coordinates of this point as tuple.'''
        return (self.x, self.y)

class Vector:
    '''Represents a vector.'''
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    @classmethod
    def from_points(cls, a : Point, b : Point):
        '''Creates a vector based on the two points a and b.'''
        return Vector(b.x - a.x, b.y - a.y)

    def length(self):
        '''Return the length of the vector.'''
        return sqrt(self.x**2 + self.y**2)

    def normal_vector(self, direction='left'):
        '''Return the left or right normal vector.'''
        if direction == 'left':
            return Vector(-self.y, self.x)
        else:
            return Vector(self.y, -self.x)
    
    def normalize(self):        
        '''Return a vector with the same direction, but with length=1.'''
        return self.multiply(1.00/self.length())
    
    def multiply(self, f: float):
        '''Return a vector that is multiplied with the number f.'''
        return Vector(self.x * f, self.y * f)

    def scalar_product(self, v2: 'Vector'):
        '''Return the scalar product of this vector and vector v2.'''
        return self.x*v2.x + self.y*v2.y

    def angle(self, v2: 'Vector'):
        '''Return the angle between this vector and vector v2.'''
        return degrees(acos( self.scalar_product(v2) / (self.length() * v2.length()) ))

    def __iter__(self):
        return [self.x, self.y].__iter__()

class Line:
    '''Represents a line.'''
    def __init__(self, p1: Point, p2: Point):
        self.a = p1
        self.b = p2

    def inline(self, p, tolerance = 0):
        '''Return True if the point is on the line.'''
        return min(self.a.x, self.b.x)-tolerance <= p.x <= max(self.a.x, self.b.x)+tolerance and min(self.a.y, self.b.y)-tolerance <= p.y <= max(self.a.y, self.b.y)+tolerance

    def intersection(self, line2, treat_as_line_segments=True):
        '''Return the intersection point of this line and line2 or None.'''
        line1 = self

        denominator = (line2.b.y - line2.a.y)*(line1.b.x - line1.a.x) - (line2.b.x - line2.a.x)*(line1.b.y - line1.a.y)

        # if parallel
        if denominator == 0:
            return None

        numerator = (line2.b.x - line2.a.x)*(line1.a.y - line2.a.y) - (line2.b.y - line2.a.y)*(line1.a.x-line2.a.x)

        ua = numerator/denominator
        s = Point(line1.a.x + ua*(line1.b.x-line1.a.x), line1.a.y + ua*(line1.b.y-line1.a.y))
        
        if not treat_as_line_segments or (line1.inline(s, tolerance=2) and line2.inline(s, tolerance=2)):
            return s
        else:
            return None

    def length(self):
        '''Return the length of this line.'''
        return Vector.from_points(self.a, self.b).length()

    def __iter__(self):
        return [self.a, self.b].__iter__()

    def __repr__(self):
        return self.a.__repr__() + " -- " + self.b.__repr__()
