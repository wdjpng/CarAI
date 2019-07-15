import tkinter


canvas = tkinter.Canvas(width=800, height=600,  background="yellow green")
canvas.pack()
canvas.update()

canvas.create_text(100,10, text='press [s] to print track on console')

points = []
lastpoint = None


def drawpoint(event):
    global points
    lastpoint = points[-1] if len(points) > 0 else None
    x = event.x
    y = event.y
    
    points.append((x,y))

    print(f'new point at: {x},{y}')    
    canvas.create_oval(x-2, y-2, x+2, y+2)

    if lastpoint is not None:
        canvas.create_line(*lastpoint, x,y)


def save(event):
    print("points:")
    for p in points:
        print(f'({p[0]},{p[1]}),', end=" ")
    print("")

canvas.focus_force()
canvas.bind('<Button-1>', drawpoint)
canvas.bind('<s>', save)

tkinter.mainloop()
