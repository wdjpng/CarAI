import tkinter
from lib.tracks import Track
from lib.car import Car
from brains import ParameterEvolutionBrain
from random import uniform
from random import randint
import random
from agents import ParameterEvolutionAgent
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from brains import DeepQLearningBrain
import numpy as np
from tkinter import *

class DeepQLearningCarController:
    model = Sequential()

    def __init__(self):

        self.canvas = tkinter.Canvas(width=800, height=600, background="yellow green")
        self.canvas.pack()
        self.level = 6

        # load track
        self.track = Track.level(self.canvas, draw_midline=True, level_number=self.level)
        self.track.draw()
        self.tickSpeed = 1
        self.isFree = True
        self.state = np.array([3.0, 4.0, 5.0])
        self.car = Car(self.track, DeepQLearningBrain(), self.level)

        self.epochs = 1000
        self.gamma = 0.9  # since it may take several moves to goal, making gamma high
        self.epsilon = 1

        self.currentEpisode = 1

    def initNeuralNetwork(self):
        DeepQLearningCarController.model.add(Dense(164, init='lecun_uniform', input_shape=(3,)))
        DeepQLearningCarController.model.add(Activation('relu'))
        # DeepQLearningCarController.model.add(Dropout(0.2)) I'm not using dropout, but maybe you wanna give it a try?

        DeepQLearningCarController.model.add(Dense(150, init='lecun_uniform'))
        DeepQLearningCarController.model.add(Activation('relu'))
        # DeepQLearningCarController.model.add(Dropout(0.2))

        DeepQLearningCarController.model.add(Dense(3, init='lecun_uniform'))
        DeepQLearningCarController.model.add(Activation('linear'))  # linear output so we can have range of real-valued outputs

        rms = RMSprop()
        DeepQLearningCarController.model.compile(loss='mse', optimizer=rms)
        

    def update(self):
        # We are in self.state S
        # Let's run our Q function on S to get Q values for all possible actions
        qval = DeepQLearningCarController.model.predict(self.state.reshape(1, 3), batch_size=1)
        if (random.random() < self.epsilon):  # choose random action
            action = np.random.randint(0, 3)
        else:  # choose best action from Q(s,a) values
            action = (np.argmax(qval))
        # Take action, observe new self.state S'
        new_state = self.makeMove(self.state, action)
        # Observe reward
        reward = self.getReward(new_state)
        # Get max_Q(S',a)
        newQ = DeepQLearningCarController.model.predict(new_state.reshape(1, 3), batch_size=1)
        maxQ = np.max(newQ)
        y = np.zeros((1, 3))
        y[:] = qval[:]
        if not self.car.isalive:  # non-terminal self.state
            update = (reward + (self.gamma * maxQ))
        else:  # terminal self.state
            update = reward
        y[0][action] = update  # target output
        print("Game #: %s" % (self.currentEpisode,))
        DeepQLearningCarController.model.fit(self.state.reshape(1, 3), y, batch_size=1, nb_epoch=1, verbose=1)
        self.state = new_state
        if not self.car.isalive:
            self.currentEpisode+=1
            self.car.removeFromCanvas()
            self.car = Car(self.track, DeepQLearningBrain(), self.level)
            if self.epsilon > 0.1:
                self.epsilon -= (1 / self.epochs)


        self.canvas.after(1, self.update)


    def getReward(self, car):
        return self.car.reward

    def makeMove(self, state, action):
        self.car.brain.action = action

        self.car.update()
        self.car.draw()

        frontCenterNormalized = 0
        frontLeftNormalized = 0
        frontRightNormalized = 0
        try:
            frontCenterNormalized = 1.0/self.car.brain.front_center_sensor.distance
        except:
            frontCenterNormalized = 1

        try:
            frontLeftNormalized = 1.0 / self.car.brain.front_left_sensor.distance
        except:
            frontLeftNormalized = 1

        try:
            frontRightNormalized = 1.0/self.car.brain.front_right_sensor.distance
        except:
            frontRightNormalized = 1

        return np.array([frontCenterNormalized, frontLeftNormalized, frontRightNormalized])

    def run(self):

        self.initNeuralNetwork()

        self.update()
        tkinter.mainloop()


class ParameterEvolutionCarController:
    def __init__(self):
        self.numberOfGeneration = 2
        self.cars = []
        self.canvas = tkinter.Canvas(width=800, height=600, background="yellow green")
        self.canvas.pack()
        self.level = 3

        # load track
        self.track = Track.level(self.canvas, draw_midline=True, level_number=self.level)
        self.track.draw()
        self.counter = 0
        self.tickSpeed = 1
        self.sizeOfOneGeneration = 50
        self.isFree = True
        self.genCounter = 1

        
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

        print('Generation ' + str(self.genCounter) + 'hatte den besten Reward ' + str(self.cars[0].totalReward))
        print('\n')


        for x in range(0, 5):
            if(x + 1 >= len(self.cars)):
                break
            self.cars[x].color = 'green'
            bestCars.append(self.cars[x])

        self.cars = []
        for x in range(0, self.sizeOfOneGeneration-6):
            newAgent = bestCars[randint(0,len(bestCars)-1)].brain.agent.uniform(bestCars[randint(0, len(bestCars) - 1)].brain.agent)
            newAgent.mutate()

            self.cars.append(Car(self.track, ParameterEvolutionBrain(newAgent), self.level))

        self.isFree = True



    def simulateGens(self):
       for x in range(0, self.numberOfGeneration - 1):
           for x in range(0, self.sizeOfOneGeneration):
               a = uniform(0, 100)
               if (a < 25):
                   self.cars.append(Car(self.track, ParameterEvolutionBrain(ParameterEvolutionAgent.randomAgent()), self.level, color="red"))
               elif a < 50:
                   self.cars.append(Car(self.track, ParameterEvolutionBrain(ParameterEvolutionAgent.randomAgent()), self.level, color="red"))
               elif a < 75:
                   self.cars.append(Car(self.track, ParameterEvolutionBrain(ParameterEvolutionAgent.randomAgent()), self.level, color="red"))
               else:
                   self.cars.append(Car(self.track, ParameterEvolutionBrain(ParameterEvolutionAgent.randomAgent()), self.level, color="red"))
       self.update()
       tkinter.mainloop()

