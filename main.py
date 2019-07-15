#
# MAIN PROGRAM
#
# Execute this script to start the simulation:
#    py main.py
#
import tkinter
from lib.tracks import Track
from lib.car import Car
import brains


# create canvas for drawing
canvas = tkinter.Canvas(width=800, height=600, background="yellow green")
canvas.pack()

# load track
track = Track.level(canvas, draw_midline=True, level_number=1)
track.draw()

# create car
car = Car(track, brains.UglyBrain(), color="blue")

def update():
    '''Update the car and redraw it.'''
    car.update()
    car.draw()

    # increase value to slow down total speed of simulation
    canvas.after(60, update) 


# start update & mainloop of window
update()
tkinter.mainloop()
