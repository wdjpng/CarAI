import tkinter
from lib.tracks import Track
from lib.car import Car
from brains import UglyBrain
from random import uniform
from random import randint
from agent import Agent

class CarController:
    def __init__(self):
        self.numberOfGeneration = 2
        self.cars = []
        self.canvas = tkinter.Canvas(width=800, height=600, background="yellow green")
        self.canvas.pack()
        self.level = 2

        # load track
        self.track = Track.level(self.canvas, draw_midline=True, level_number=self.level)
        self.track.draw()
        self.counter = 0
        self.tickSpeed = 1
        self.sizeOfOneGeneration = 50
        self.isFree = True

        
    def update(self):
        if(self.isFree):
            self.counter = self.counter + 1

            for x in range(0, len(self.cars) - 1):
                self.cars[x].update()
                self.cars[x].draw()

            self.canvas.after(self.tickSpeed, self.update)

            if (self.counter > 500):
                self.counter = 0
                self.isFree = False
                self.updateCars()


    def getReward(self, car):
        Track.level(1).midline_points

    def updateCars(self):
        self.cars.sort()
        bestCars=[]


        for x in range(0, 5):
            self.cars[x].color = 'green'
            bestCars.append(self.cars[x])

        self.cars = []


        for x in range(0, 4):
            self.cars.append(bestCars[x])
        for x in range(0, self.sizeOfOneGeneration-6):
            newAgent = bestCars[randint(0,4)].brain.agent.uniform(bestCars[randint(0,4)].brain.agent)
            newAgent.mutate()

            self.cars.append(Car(self.track, UglyBrain(newAgent), self.level))

        self.isFree = True



    def simulateGens(self):
       for x in range(0, self.numberOfGeneration - 1):
           for x in range(0, self.sizeOfOneGeneration):
               a = uniform(0, 100)
               if (a < 25):
                   self.cars.append(Car(self.track, UglyBrain(Agent.randomAgent()), self.level, color="red"))
               elif a < 50:
                   self.cars.append(Car(self.track, UglyBrain(Agent.randomAgent()), self.level, color="red"))
               elif a < 75:
                   self.cars.append(Car(self.track, UglyBrain(Agent.randomAgent()), self.level, color="red"))
               else:
                   self.cars.append(Car(self.track, UglyBrain(Agent.randomAgent()), self.level, color="red"))
       self.update()
       tkinter.mainloop()

