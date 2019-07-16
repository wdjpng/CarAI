from random import uniform


class Agent:

    def __init__(self, stoppingConstant, acceletationConstant, maxSpeed, horizontalAccelerationConstant,
                 horizontalAccelerationConstant2):
        self.stoppingConstant = stoppingConstant
        self.acceletationConstant = acceletationConstant
        self.maxSpeed = maxSpeed
        self.horizontalAccelerationConstant = horizontalAccelerationConstant
        self.horizontalAccelerationConstant2 = horizontalAccelerationConstant2
        self.mutationRate = 0.1

    def mutate(self):
        self.stoppingConstant += self.stoppingConstant * uniform(-self.mutationRate, self.mutationRate)
        self.acceletationConstant += self.acceletationConstant * uniform(-self.mutationRate, self.mutationRate)
        self.maxSpeed += self.maxSpeed * uniform(-self.mutationRate, self.mutationRate)
        self.horizontalAccelerationConstant += self.horizontalAccelerationConstant * uniform(-self.mutationRate,
                                                                                             self.mutationRate)
        self.horizontalAccelerationConstant2 += self.horizontalAccelerationConstant2 * uniform(-self.mutationRate,
                                                                                               self.mutationRate)
        return self

    def uniform(self, agent):
        return Agent((self.stoppingConstant + agent.stoppingConstant) / 2,
                     (self.acceletationConstant + agent.acceletationConstant) / 2,
                     (self.maxSpeed + agent.maxSpeed) / 2,
                     (self.horizontalAccelerationConstant + agent.horizontalAccelerationConstant) / 2,
                     (self.horizontalAccelerationConstant2 + agent.horizontalAccelerationConstant2) / 2).mutate()

    @staticmethod
    def randomAgent():
        return Agent(uniform(0, 50), uniform(0, 10), uniform(0, 6), uniform(0, 0.2), uniform(0, 100))
