import pymunk
import pygame
import math
import random

# PYGAME INITIALISE
pygame.init()
clock = pygame.time.Clock()
width, height = 1280, 720
icon = pygame.image.load("favicon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Pyvlov's Dog - Simulation")


# If you don't know pymunk, a body tracks the momentum and location of an object,
#  and a shape is attached to it for collsions


class Collision_Handler:
    """
    handles a collision. allows for localised collisions that result in something, like an ldr to act like a sensor

    An object type, as described throughout, is an integer. it allows for a collision check to be done by comparing the
    two types and determining if there is a special case involved

    Presolve triggers continuously after collision and before the objects separate. It triggers the response function
    during this.
    """

    def __init__(self, simulation, object1, object2, outcome):
        self.sim = simulation
        self.handler = simulation.space.add_collision_handler(object1, object2)
        self.outcome = outcome
        self.handler.pre_solve = self.response

    def response(self, arbiter, space, data):
        """
        the function called when the collision occurs. Modifies the simulations input into the neural network.
        """
        if self.outcome == "punish":
            self.sim.punish = True
        if self.outcome == "reward":
            self.sim.reward = True
        return True


class Dog_Part:
    """
    A component of the dog. Something like a wheel or a sensor.

    shape describes the object in terms of its actual shape, rather than position. For instance a square would be

    [(0, 0), (x, 0), (x, x), (0, x)]

    Displacement is relative position to the body. At (0, 0) the top left corner of the shape will align with the body.

    Sensor is whether or not the object is collidable or not. A non-collidable object is still able to trigger a
    collision handler at an intersection, but the environment will ignore it in terms of physics interactions.

    Collision type is an integer used for tracking interactions, as outlined above.

    Colour is, the colour of the object in [R, G, B] form.

    Wheel is a preset variable. If it is set to "L" the object is treated as a left wheel, and if it is set to "R" it is
    treated as a right wheel.
    """

    def __init__(self, shape_vertices, displacement, sensor, collision_type, colour, wheel="N"):
        self.shape_vertices = shape_vertices
        self.displacement = displacement
        self.local_coordinates = self.get_local_vertices()
        self.sensor = sensor
        self.collision_type = collision_type
        self.colour = colour
        self.wheel = wheel

        self.shape = pymunk.Poly(None, self.local_coordinates, radius=0.5)
        self.shape.collision_type = self.collision_type
        self.shape.sensor = self.sensor

    def get_local_vertices(self):
        """
        Adds the displacement of the shape to the shapes vertices to return the local coordinates of it
        """
        vertices = []
        dx, dy = self.displacement[0], self.displacement[1]
        for point in self.shape_vertices:
            new_x = point[0] + dx
            new_y = point[1] + dy
            vertices.append((new_x, new_y))
        return vertices

    def get_global_vertices(self):
        """
        gets the global vertices of the shape
        """
        vertices = []
        bx = self.shape.body.position[0]
        by = self.shape.body.position[1]
        for v in self.shape.get_vertices():
            rotated = v.rotated(self.shape.body.angle)
            vertices.append((rotated[0] + bx, rotated[1] + by))
        return vertices

    def get_local_point(self):
        """
        Gets the local coordinates of the centre of the part, relative to the body
        """
        dx = self.displacement[0]
        dy = self.displacement[1]
        centre = (self.get_width() / 2 + dx, self.get_height() / 2 + dy)
        return centre

    def draw(self, simulation):
        """
        draws the individual part
        """
        pygame.draw.polygon(simulation.screen, self.colour, self.get_global_vertices())

    def get_width(self):
        """
        Gets the maximum width of the object
        """
        width = 0
        for vertex in self.shape_vertices:
            if vertex[0] > width:
                width = vertex[0]
        return width

    def get_height(self):
        """
        Gets the maximum height of the object
        """
        height = 0
        for vertex in self.shape_vertices:
            if vertex[1] > height:
                height = vertex[1]
        return height

    def get_circumference(self):
        """
        Gets the circumference, presuming the object is a wheel
        """
        diameter = self.get_height()
        circumference = diameter * math.pi
        return circumference

    def apply_force(self, force):
        """
        applies a force of the magnitude prescribed to the object, upwards in terms of local coordinates
        """
        self.shape.body.apply_impulse_at_local_point(force, self.get_local_point())


class Dog:
    """
    The dog simulated by the simulation.

    Parts is a list containing Dog_Part objects. The parts are added to the dogs body and it is as a whole treated as one
    object by the simulation.

    """

    def __init__(self, parts):
        # TODO Dog Stuff
        self.body = pymunk.Body(1, 1)
        self.body.position = (width / 2, height / 2)
        self.parts = []
        self.left_wheels = []
        self.right_wheels = []
        for part in parts:
            self.attach_part(part)
            self.parts.append(part)
            if part.wheel == "L":
                self.left_wheels.append(part)
            if part.wheel == "R":
                self.right_wheels.append(part)

    def attach_part(self, part):
        """
        Attaches a part to the dog
        """
        part.shape.body = self.body
        self.parts.append(part)

    def draw(self, simulation):
        """
        draws each individual part of the dog into the pygame window
        """
        for part in self.parts:
            part.draw(simulation)
        position = []
        position.append(int(self.body.position[0]))
        position.append(int(self.body.position[1]))
        pygame.draw.circle(simulation.screen, [255, 0, 0], position, 4)

    def apply_wheel_force(self, left_rpm, right_rpm):
        """
        applies the wheel velocities to all of the wheels.
        """
        for part in self.left_wheels:
            displacement = -left_rpm * part.get_circumference()

            part.apply_force((0.00, displacement))
        for part in self.right_wheels:
            displacement = -right_rpm * part.get_circumference()
            part.apply_force((0.00, displacement))


class Object_Type:
    """
    An object type for the purposes of the simulation
    """

    def __init__(self, colour, collide, collision_type):
        self.colour = colour
        self.collide = collide
        self.collision_type = collision_type


class Object_Instance:
    """
    An instance of an object type for the simulation
    """

    def __init__(self, type, size, position, simulation):
        # Instantiates the basic components of the object
        self.colour = type.colour
        self.collide = type.collide
        self.collision = type.collision_type
        self.size = size
        self.position = position
        self.simulation = simulation

        # Handles the PyMunk parts of the object
        self.body = pymunk.Body(1, 0, pymunk.Body.STATIC)
        self.body.position = self.position
        self.shape = pymunk.Poly.create_box(self.body, (self.size, self.size), radius=1)
        self.shape.collision_type = self.collision
        self.simulation.space.add(self.body, self.shape)

    def get_vertices(self):
        """
        Finds the local coordinates of the shape, adds the body's position to them and returns it as a list.
        """
        vertices = []
        bx = self.body.position[0]
        by = self.body.position[1]
        for v in self.shape.get_vertices():
            vertices.append((v[0] + bx, v[1] + by))
        return vertices

    def draw(self):
        """
        Draws the object on the pygame screen
        """
        pygame.draw.polygon(self.simulation.screen, self.colour, self.get_vertices())


class Simulation:
    """
    A simulation instance for the purpose of replicating the dogs movement, and visually displaying this
    to the user.
    """

    def __init__(self):
        self.space = pymunk.Space()
        self.collision_shapes = []
        self.simulation_objects = []
        self.collision_handlers = []
        self.set_boundaries()
        self.dog = None
        self.punish = 0
        self.reward = 0
        self.has_quit = False
        self.screen = pygame.display.set_mode((width, height))

    def set_boundaries(self):
        """
        Creates the boundary walls of the simulation. These align with the screen borders.

        Each boundary is added in the following pattern:

        create body
        create segment
        set body position
        add the segment and body to the space

        The body controls the position and momentum of an object in the simulation. The segment is stationary, but it is
        still required. Next the segment is created and attached to the body. This contains the dimensions of the shape.
        The body is then moved to the correct position and placed into the simulation.
        """

        self.top_boundary_body = pymunk.Body(1, 0, pymunk.Body.STATIC)
        self.top_boundary_segment = pymunk.Segment(self.top_boundary_body, (0, 0), (width, 0), 2)
        self.top_boundary_body.position = (0, 0)
        self.space.add(self.top_boundary_body, self.top_boundary_segment)

        self.right_boundary_body = pymunk.Body(1, 0, pymunk.Body.STATIC)
        self.right_boundary_segment = pymunk.Segment(self.right_boundary_body, (0, 0), (0, height), 2)
        self.right_boundary_body.position = (width, 0)
        self.space.add(self.right_boundary_body, self.right_boundary_segment)

        self.left_boundary_body = pymunk.Body(1, 0, pymunk.Body.STATIC)
        self.left_boundary_segment = pymunk.Segment(self.left_boundary_body, (0, 0), (0, height), 2)
        self.left_boundary_body.position = (0, 0)
        self.space.add(self.left_boundary_body, self.left_boundary_segment)

        self.bottom_boundary_body = pymunk.Body(1, 0, pymunk.Body.STATIC)
        self.bottom_boundary_segment = pymunk.Segment(self.bottom_boundary_body, (0, 0), (width, 0), 2)
        self.bottom_boundary_body.position = (0, height)
        self.space.add(self.bottom_boundary_body, self.bottom_boundary_segment)

    def add_static_body(self, type, size, location):
        """
        This adds a static body to the simulation to be collided with by the Dog.
        """
        obj = Object_Instance(type, size, location, self)
        self.simulation_objects.append(obj)
        self.collision_shapes.append(obj)

    def add(self, object):
        """
        Adds an individual object to the simulation
        """
        self.space.add(object)

    def step(self, time, left_rpm, right_rpm):
        """
        This steps the space for the time specified
        """
        if self.dog != None:
            self.dog.apply_wheel_force(left_rpm, right_rpm)
            self.space.step(time)
            self.dog.body.velocity = (0, 0)
            self.dog.body.angular_velocity = 0
            self.space.step(time)
        # print(self.punish, self.reward)
        self.punish, self.reward = False, False

    def draw_simulation_objects(self):
        """
        This draws the shapes within the simulation into the pygame window
        """
        self.screen.fill([0, 90, 0])
        for object in self.simulation_objects:
            object.draw()

    def add_dog(self, parts):
        """
        adds the dog into the simulation
        """
        self.dog = Dog(parts)
        self.space.add(self.dog.body)
        for part in parts:
            self.space.add(part.shape)

    def draw_dog(self):
        """
        draws the dog into the pygame window
        """
        if self.dog != None:
            self.dog.draw(self)

    def display_update(self, is_dog):
        """
        updates the pygame window
        """
        self.draw_simulation_objects()
        self.draw_dog()
        pygame.display.update()

    def input_network(self):
        """
        polls the neural network with the input data to get the next step
        to access the punish/reward things right now use self.punish and self.reward. they will be equal to the
        current values

        please set this up to poll the network with the inputs and
        """
        left_wheel = 0.01  # random.randint(0, 10)/1000
        right_wheel = 0.01  # random.randint(0, 10)/1000
        return (left_wheel, right_wheel)

    def add_collision_handler(self, object_type_1, object_type_2, outcome):
        """
        Creates a collision handler object in the simulation so as to allow the user to create rules between
        object interactions
        """
        self.collision_handlers.append(Collision_Handler(self, object_type_1, object_type_2, outcome))

    def event_queue(self):
        """
        the pygame event queue. Used to allow the user to quit the pygame window
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.has_quit = True
                pygame.quit()
                break


"""
Here is a demonstration case of the simulation working. 
This simulation is complete, it just needs integration with the GUI
The unintegrated version of the project that allows for this is in the folder "unintegrated"

Don't click anything in the simulation, it will freeze because windows
will think it's not responding due to a crash not deliberately
"""
#
# black = [0, 0, 0]
# brown = [90, 90, 30]
# yellow = [255, 255, 0]
#
# #Creates the simulation
#
# sim = Simulation()
#
# #Defines the object type light, and creates two instances of it
#
# light = Object_Type([255, 255, 0], True, 1)
# sim.add_static_body(light, 50, (640, 200))
# sim.add_static_body(light, 50, (40, 40))
#
# #Creates the dog parts, as explained above
#
# chassis = Dog_Part([(0, 0), (50, 0), (50, 100), (0, 100)], (-25, -25), False, 0, brown)
#
# left_wheel = Dog_Part([(0, 0), (10, 0), (10, 30), (0, 30)], (-36, -20), False, 0, black, wheel="L")
# right_wheel = Dog_Part([(0, 0), (10, 0), (10, 30), (0, 30)], (26, -20), False, 0, black, wheel="R")
# b_left_wheel = Dog_Part([(0, 0), (10, 0), (10, 30), (0, 30)], (-36, 35), False, 0, black, wheel="L")
# b_right_wheel = Dog_Part([(0, 0), (10, 0), (10, 30), (0, 30)], (26, 35), False, 0, black, wheel="R")
#
# ldr = Dog_Part([(0, 0), (50, 0), (50, 6), (0, 6)], (-25, -35), True, 2, yellow)
# ultra_sonic = Dog_Part([(0, 0), (6, 0), (6, 40), (0, 40)], (-3, -65), True, 3, black)
#
# dog_parts = [chassis, left_wheel, right_wheel, b_left_wheel, b_right_wheel, ldr, ultra_sonic]
# sim.add_dog(dog_parts)
#
# #Creates a rule punishing the dog for contacting the LDR with light.
#
# sim.add_collision_handler(2, 1, "punish")
#
# while True:
# #Feeds the neural network the current inputs, and receives the wheel rpms
#     wheel_values = sim.input_network()
# #Steps the simulation, and applies the wheel values to it
#     sim.step(0.01, wheel_values[0], wheel_values[1])
# #Updates the display
#     sim.display_update(True)
