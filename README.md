# PyVlovs_Dog_
This is PyVlov's Dog, a software package designed to enable a user to recreate classical conditioning within a controlled simulation, on whatever algortithm they desire! This was created as a 12th grade school project.

## How it Works
The software package involves a user friendly simulation software, a dog creation kit as well as two different dog-controlling algorithms for a quick start. In a general use case a user will first create a dog in the dog creation kit. This piece of software allows a user to replicate an existing robot, or build one from the ground up. It is easy to use and understand, with several examples included in the package. Next, the user will load up the simulation. They will come to the launcher window. From here, a user can create rules, objects and change the simulation or dog in use. Once done, a user closes the window, automatically opening the simulation and the run-time GUI. The run-time GUI allows the placement of objects in the simulation, simply set the size, click the add button, and click on the simulation where you want the objects to be. To exit the program close the Python terminal window. To return to the launcher, close either window normally.

## FAQ
### Why is the colour I am entering being turned to black/causing an error?
Currently, the software uses two different colour formats. In the dog creation kit colours are entered in the [R, G, B] format, with each of the codes being a decimal value between 0 and 255. In the simulation's object creation window, colour is entered as #RRGGBB format, with each of the 2 digit codes in hexadecimal, case insensitive. 

### What do you mean by sensor?
Sensor is terminology borrowed from PyMunk, referring to whether or not an object is treated as solid. An object marked as sensor will allow objects to pass through it, but will still trigger any collision handlers attached to it.

### What is an object type?
Once more this is terminology borrowed from PyMunk. An objects type is a numerical category used for handling collisions. For instance, an object created by the player may be labelled as a type 5, and a part of the dog's chassis labelled type 7. A user may create a rule rewarding/punishing collsions between type 5s and 7s, which will be triggered on their contact. By default things are assigned type 0. For that reason we discourage using type 0 in rules, as it will trigger on the boundary walls, among other things. 

### The dog disappeared!
The physics engine (PyMunk) uses a stepped collision algorithm. As such, if the simulation speed is set too high, the dog may travel past the objects between it and the region outside of the window, as that is its projected motion in that time frame. To avoid this, we recommend keeping the simulation speed lower.

### I want to create my own algorithm for controlling the dog, how do I do it?
Simply create a python file with a function including the following function:
```
def interact(punish, reward):
    <your algorithm here>
    return (left_wheels, right_wheels)
```
Then, when running the program, change the path in the launcher settings menu to the path of the file. The program will execute your function to find the wheel velocities, so include within it all needed steps between iterations.

## Libraries Used
- AST
  - Used for the literaleval function, so as to be able to take user entered lists and directly convert them to lists.
- Tkinter
  - Used for launcher GUI and Run-Time GUI.
- OS
  - Checking if the directory exists for the dog creation kits save function, and making it if it doesn't.
- PIL
  - Creating the image of the dog used in the dog creation kit.
- PyGame
  - Used for the simulation GUI.
- PyMunk
  - Used for simulating physics in the simulation.
- Math
  - Used for PI.
- importlib
  - Used for importing the selected algorithm's file.
