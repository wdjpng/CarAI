# CarAI
## What this repo is
This source code provides you with a car simulation as well as some methods to control the cars in it. A simulation contains a track,
a car and an Artificial Intelligence (the Brain), which controls the car. More complex controls methods such as evolution or deep q learning are 
additionally handled by a car controller. There are six default tracks, new ones can be generated with the trackeditor.py.

The implementation of the car simulation per se is separeted into the following files
- lib/car.py: The car class
- lib/math2d.py: Classes and methods to deal with the math needed for the simulation
- lib/sensors.py: Sensors to measure distance
- lib/tracks.py: The different tracks the car can drive on.

## Usage
First install the required pip packages and clone this repository
```
pip install keras numpy tensorflow tkinter 

git clone https://github.com/wdjpng/CarAI
```

Then run the main method
```
cd /your_path/CarAI/
python main.py
```

This will run the car controller, by default the deep q learning car controller. 

Now a deep q learning network trains, you should see a window like this:

[![car_on_track_screenshot](https://i.postimg.cc/DwSyqHG6/Screenshot-2019-07-19-12-35-03.png)](https://postimg.cc/k2dmCjfR)

## Reccomended learning resources
If you dont know what deep q learning, reinforcment learning and neural networks are I highly recommend watching
[3blue1brown's series on neural networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) 
as well as reading [this](http://outlace.com/rlpart1.html) article as well as its other parts on reinforcment learning.

## Sources
The lib and the solution folders as well as some other files were coded by the [ComputerCamp](https://www.computercamp.at/). They have the full rights for all the 
intellectual property provided in these folders. My part is the Deep Q Learning brain, the agent, the evoultion brain and the car controller
