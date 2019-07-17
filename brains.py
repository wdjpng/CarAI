#
# BRAINS
#
# Add in this file your brain class. Look at the two example brains for inspiration.
#
from lib.car import Brain
from lib.sensors import Sensor, GoalSensor
import random
from agent import Agent
class InteractiveBrain(Brain):
	"""Brain that allows to control a car with the arrow keys."""
	def setup(self):
		def up(event):
			self.car.accelerate(1)

		def down(event):
			self.car.accelerate(-1)

		def right(event):
			self.car.turn(15)

		def left(event):
			self.car.turn(-15) 

		self.track.canvas.focus_force()  # listen

		self.track.canvas.bind('<Up>', up)
		self.track.canvas.bind('<Down>', down)
		self.track.canvas.bind('<Right>', right)
		self.track.canvas.bind('<Left>', left)

	def update(self):
		pass


class InteractiveBrainWithSensors(Brain):
	"""Brain that allows to control a car with the arrow keys and that installs sensors on the car."""
	def setup(self):
		super(InteractiveBrainWithSensors, self).setup()
		
		self.front_left_sensor = Sensor(self.car, angle=-2, x=-6, y=15)
		self.front_center_sensor = Sensor(self.car, angle=0, x=0, y=15)
		self.front_right_sensor = Sensor(self.car, angle=2, x=6, y=15)
		self.goal_sensor = GoalSensor(self.car)       

	def update(self):
		print(self.car.sensors)
		print(f"[sensor] distance: {self.front_center_sensor.distance}, is_goal: {self.front_center_sensor.is_obstacle_goal}")
		print(f"[car] speed: {self.car.speed}, direction: {self.car.direction}")

class RandomBrain(Brain):
	"""Brain that allows to control a car with the arrow keys."""
	def up(event):
			self.car.accelerate(1)

	def down(event):
		self.car.accelerate(-1)

	def right(event):
		self.car.turn(15)

	def left(event):
		self.car.turn(-15) 
		
	def update(self):

		if(random.randint(0,100) > 20):
			self.car.accelerate(0.5)
		if(random.randint(0,100) > 80):
			self.car.accelerate(-0.5)
		if(random.randint(0,100) > 70):
			self.car.turn(-2)
		if(random.randint(0,100) > 70):
			self.car.accelerate(2)
		pass


class ParameterEvolutionBrain(Brain):

	def __init__(self, agent):
		self.agent = agent
		self.stoppingContant = agent.stoppingConstant
		self.acceletationConstant = agent.stoppingConstant
		self.maxSpeed = agent.maxSpeed
		self.horizontalAccelerationConstant = agent.horizontalAccelerationConstant
		self.horizontalAccelerationConstant2 = agent.horizontalAccelerationConstant2


	def setup(self):
		self.i = 0
		self.front_left_sensor = Sensor(self.car, angle=-90, x=-6, y=15)
		self.front_center_sensor = Sensor(self.car, angle=0, x=0, y=15)
		self.front_right_sensor = Sensor(self.car, angle=90, x=6, y=15)
		self.goal_sensor = GoalSensor(self.car)

	def update(self):
		self.i+=1

		frontUrgency = 10/self.front_center_sensor.distance
		rightUrgency = 20/self.front_right_sensor.distance
		leftUrgency = 20/ self.front_left_sensor.distance
		if(frontUrgency < 0 | self.front_center_sensor.is_obstacle_goal):
			frontUrgency = 0
		if(rightUrgency < 0):
			rightUrgency = 0
		if(leftUrgency < 0):
			leftUrgency = 0

		leftUrgency*=leftUrgency
		rightUrgency*=rightUrgency



		self.car.accelerate(-self.stoppingContant*frontUrgency)
		if(self.car.speed < self.maxSpeed):
			self.car.accelerate(self.acceletationConstant)

		if(self.front_center_sensor.is_obstacle_goal):
			self.car.accelerate(2)
		self.car.turn(-self.front_right_sensor.distance * self.horizontalAccelerationConstant)
		self.car.turn(self.front_left_sensor.distance * self.horizontalAccelerationConstant)



		if(self.front_left_sensor.distance < 10):
			self.car.turn(self.horizontalAccelerationConstant2)
			self.car.accelerate(2)
		if(self.front_right_sensor.distance < 10):
			self.car.turn(-self.horizontalAccelerationConstant2)
			self.car.accelerate(2)

		pass
