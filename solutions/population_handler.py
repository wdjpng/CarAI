import tkinter
from lib.tracks import Track
from lib.car import Car
from solutions.brains_genetic import GeneticBrain
import random


def create_initial_population(n):
    population = []
    for i in range(0, n):
        population += [Car(track, GeneticBrain.random(), color="blue")]
    return population


def calculate_fitness(population):
    # let cars drive
    while any([c.isalive for c in population]):
        for c in [c for c in population if c.isalive]:
            c.update()
            c.draw()
            canvas.update()

    # calculate fitness of brains
    for c in population:
        c.brain.fitness()


def select_most_fitting(population):
    sorted_by_fitness = sorted(population, key=lambda x: x.brain.fitness())
    # select 20 best and 10 worst performing brains
    return sorted_by_fitness[:2]


def breed_population(parents, n):
    population = []

    for p in parents:
        brain = p.brain.clone()        
        population.append(Car(track, brain, color="blue"))
    
    while len(population) < n:
        parent = random.choice(parents)        
        child_brain = GeneticBrain()
        child_brain.script = parent.brain.script
        child_brain._parent_script_i = max(0,int(parent.brain._script_i-5))
        child_brain.mutate()
        population += [Car(track, child_brain, color="blue")]

    return population


def mutate_population(population):
    for p in population:
        p.brain.mutate()


# -----------------------------------------------------------------------------

# create canvas for drawing
canvas = tkinter.Canvas(width=800, height=600, background="yellow green")
canvas.pack()

# load track
track = Track.level(canvas, draw_midline=True, level_number=6)
track.draw()

# -----------------------------------------------------------------------------


def go():
    n = 30
    population = create_initial_population(n)

    calculate_fitness(population)
    while not any([c.brain.fitness() < 10 for c in population]):
        old_population = list(population)
        selection = select_most_fitting(population)
        population = breed_population(selection, n)        
        for i in range(0, n):
            population[i].canvas_shape_id = old_population[i].canvas_shape_id            
         
        calculate_fitness(population)


canvas.after(100, go)

tkinter.mainloop()
