#
# TRACK
#
# Contains the track class.
#
import tkinter
from lib.math2d import Point, Line, Vector

class Track:
    '''Represents the track.'''

    def __init__(self, canvas : tkinter.Canvas, draw_midline: bool, midline_points: list((int,int))):
        self.canvas = canvas   
        self.draw_midline = draw_midline
        self.midline_points = midline_points
        self.track_width = 35
    
        self.points = []
        self.lines = []
        self.startpoint = None
        self.startdirection = None
        self.endpoint = None
        self.endarea_points = None
        
        self.track_canvas_id = None
        self.goal_canvas_id = None
        self.midline_canvas_ids = None

        self.calculate_points(self.midline_points)
        
    @classmethod
    def level(cls, canvas : tkinter.Canvas, draw_midline: bool, level_number : int):
        '''Return the track of the specified level.'''
        levels = [
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
        return Track(canvas, draw_midline, levels[level_number-1])

    def calculate_points(self,midline_points):
        '''Calculate the track shape, goal and start point based on the provided midline points.'''
        inner_lines = []
        outer_lines = []

        # create inner/outer lines
        for i in range(0, len(midline_points)-1):
            a = Point(*midline_points[i])
            b = Point(*midline_points[i+1])
            v = Vector.from_points(a, b)
            left_vector = v.normal_vector(direction='left').normalize().multiply(self.track_width)
            right_vector = v.normal_vector(direction='right').normalize().multiply(self.track_width)
            outer_line = Line(a.move(left_vector.x, left_vector.y), b.move(left_vector.x, left_vector.y))
            inner_line = Line(a.move(right_vector.x, right_vector.y), b.move(right_vector.x, right_vector.y))
            inner_lines.append(inner_line)
            outer_lines.append(outer_line)
        self.lines = outer_lines + [Line(inner_lines[-1].b, outer_lines[-1].b)] + list(reversed(inner_lines)) + [Line(inner_lines[0].a, outer_lines[0].a)]

        # intersect lines        
        lines_points = []        
        for i in range(0, len(self.lines) - 1):
            l1 = self.lines[i]
            l2 = self.lines[i+1]
            s = l1.intersection(l2, treat_as_line_segments=False)
            lines_points.append(s)

        # points of track        
        self.points = [self.lines[0].a] + lines_points + [self.lines[-1].b]

        # start point (25 from start)
        self.startpoint = Point(*Vector.from_points(Point(*midline_points[0]), Point(*midline_points[1])).normalize().multiply(25)).move(*midline_points[0])        

        # start direction
        startvector = Vector.from_points(Point(*midline_points[0]), Point(*midline_points[1])).normalize()
        self.startdirection =  startvector.angle(Vector(0,1))
        self.startdirection = -(180-self.startdirection) if startvector.x <= 0 else 180 - self.startdirection
        
        # end polynom
        end_vector = Vector.from_points(Point(*midline_points[-1]), Point(*midline_points[-2])).normalize()        
        end_vector_left = end_vector.normal_vector(direction='left').multiply(self.track_width*0.80)
        end_vector_right = end_vector.normal_vector(direction='right').multiply(self.track_width*0.80)
        self.endpoint = Point(*end_vector.multiply(25)).move(*midline_points[-1])
        self.endarea_points = [
            Point(*midline_points[-1]).move(*end_vector_left).astuple(),
            self.endpoint.move(*end_vector_left).astuple(),
            self.endpoint.move(*end_vector_right).astuple(),
            Point(*midline_points[-1]).move(*end_vector_right).astuple()
        ]

    def shapes(self):
        '''Return the shapes that are used for the track.'''
        return [self.points, self.endarea_points]

    def intrack(self, x, y):       
        '''Return True if point (x,y) is within track.''' 
        return self.track_canvas_id in self.canvas.find_overlapping(x,y,x,y)

    def ingoal(self, x, y):
        '''Return True if point (x,y) is within goal.'''
        return self.goal_canvas_id in self.canvas.find_overlapping(x,y,x,y)
   
    def intersections(self, polynom, frompoint, topoint):
        '''Return intersections of the line (frompoint,topoint) with the polynom.'''
        points_of_shape = [Point(x,y) for x,y in [polynom[-1]] + polynom]
        points = []  
        
        for i in range(0,len(points_of_shape)-1):
            s = Line(frompoint, topoint).intersection(Line(points_of_shape[i], points_of_shape[i+1]))
            if s is not None:
                points.append(s)
        
        return points

    def draw(self):       
        '''Draw the track.''' 
        if self.track_canvas_id is None:
            self.track_canvas_id = self.canvas.create_polygon(*[p.astuple() for p in self.points], fill="cornsilk2")  

        if self.midline_canvas_ids is None and self.draw_midline:
            self.midline_canvas_ids = []
            for i in range(0, len(self.midline_points)-1):
                self.midline_canvas_ids.append(self.canvas.create_line(*self.midline_points[i], *self.midline_points[i+1], fill="cornsilk4", dash=(6,6), width=1))

        if self.goal_canvas_id is None:
            self.goal_canvas_id = self.canvas.create_polygon(*self.endarea_points, fill="gray50")
