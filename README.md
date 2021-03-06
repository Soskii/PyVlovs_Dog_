# PyVlovs_Dog_
This is PyVlov's Dog, a software package designed to enable a user to recreate classical conditioning within a controlled simulation, on whatever algortithm they desire! This was created as a 12th grade school project.


## What is it?

PyVlov's dog is a software package that is designed to give the user the tools to recreate classical conditioning. It allows the user to 
 - Create a custom simulated dog!
 - Import their own algorithm to act as the dogs brain.
 - Create objects in the Simulation to collide with the dog.
 - Define rules for the dog to be trained against.

## Quickstart
Just run the file <b>main_loop.py</b> to launch the program.

## Guide
### Create a Dog
To create a dog open the <b>Dog Creation Kit.py</b> file to start! If you want to view an existing dog, add "default" to the directory and click import. A dog in this program is a collection of parts. A part has a number of attributes.
- The shape's vertices.
    - The coordinates of the points making up the shape, drawn with the centre of the shape as (0, 0)
- The displacement from the origin.
    - How far the shape is displaced in the local coordinates of the dog.
- If it is a sensor.
    - Sensor is terminology borrowed from PyMunk, referring to whether or not an object is treated as solid. An object marked as sensor  will allow objects to pass through it, but will still trigger any collision handlers attached to it.
- Its object type.
    - Once more this is terminology borrowed from PyMunk. An objects type is a numerical category used for handling collisions. For     instance, an object created by the player may be labelled as a type 5, and a part of the dog's chassis labelled type 7. A user may create a rule rewarding/punishing collsions between type 5s and 7s, which will be triggered on their contact. By default things are assigned type 0. For that reason we discourage using type 0 in rules, as it will trigger on the boundary walls, among other things. 
- The colour.
    - Colour is entered into the program as a six-digit hexadecimal string, with a leading hash (#RRGGBB)
- If it is a wheel.
    - A value of L R or N for left wheel, right wheel, or not a wheel respectively.
    
At any point click update to view the current version of your dog. Once satisfied, write in the directory you want to save it under, and click export.
### Writing an Algorithm
Simply create a python file with a function called interact. Here is an example:
```
def interact(punish, reward):
    <your algorithm here>
    return (left_wheels, right_wheels)
```
Then, when running the program, change the path in the launcher settings menu to the path of the file. The program will execute your function to find the wheel velocities, so include within it all needed steps between iterations.

### Running the Simulation
Run the <b>main_loop.py</b> file. Once inside, you will see several headings: Objects, Rules and Simulator Settings.
#### Creating an Object
Objects are things in the simulation that interact with the dog. They have a colour, type and are either a sensor or not. To create an object, click the add an object button. Then, fill in the colour, in the format of "#RRGGBB", the object type and whether the object is a sensor.
#### Creating Rules
Rules are simple structures that tell the simulation how to react to a collision in terms of feedback to the algorithm. As such, it has 3 pieces of data involved. The two things colliding, and if this is good or bad. The things are referred to by their type, such as a dog part of type 2 colliding with a object of type 4. If it is good or bad is defined by the punish/reward radial buttons on the right.
#### Simulator Settings
First, you must be sure that the paths written in the simulator settings are the paths of the dog and algorithm you want to use. Next, you may adjust the speed to one that you believe is suitable for your purposes.

<b>Once you have completed all this, close the window with the X in the corner, to open the simulation.</b>

### The Simulation Proper
You will now see the dog on the screen, being controlled by the network. To interact with the network, you can add instances of an object you have created into the environment using the run-time settings window. Adjust its size and click add. Now, wherever you click in the simulation an object of that size and characteristics will appear.

To return to the settings menu, close either window.

## FAQ
### Why is the colour I am entering being turned to black/causing an error?
Colour is entered into the program as a six-digit hexadecimal string, with a leading hash (#RRGGBB). Inputing it in a different format will result in errors. 

### What do you mean by sensor?
Sensor is terminology borrowed from PyMunk, referring to whether or not an object is treated as solid. An object marked as sensor will allow objects to pass through it, but will still trigger any collision handlers attached to it.

### What is an object type?
Once more this is terminology borrowed from PyMunk. An objects type is a numerical category used for handling collisions. For instance, an object created by the player may be labelled as a type 5, and a part of the dog's chassis labelled type 7. A user may create a rule rewarding/punishing collsions between type 5s and 7s, which will be triggered on their contact. By default things are assigned type 0. For that reason we discourage using type 0 in rules, as it will trigger on the boundary walls, among other things. 

### The dog disappeared!
The physics engine (PyMunk) uses a stepped collision algorithm. As such, if the simulation speed is set too high, the dog may travel past the objects between it and the region outside of the window, as that is its projected motion in that time frame. To avoid this, we recommend keeping the simulation speed lower.

### How do I exit the program?
The quit button is at the bottom of the settings menu in the launcher.

### It's crashing, help!
There are a few possible reasons it could crash. The first is running the file from an improper location. <b>The file must be run from the folder it is in.</b> The next is not filling in parts of the gui. If certain things are not filled in, such as leaving object types blank in a rule, will result in a crash.

## Libraries Used
- AST
  - Used for the literaleval function, so as to be able to take user entered lists and directly convert them to lists.
- Tkinter
  - Used for launcher GUI, Run-Time GUI and Dog Creation Kit.
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
