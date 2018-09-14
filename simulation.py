import pymunk
import pygame

# PYGAME INITIALISE
pygame.init()
clock = pygame.time.Clock()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load("favicon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Pyvlov's Dog - Simulation")


class Rule:
    """
    A user created rule that the network is trained to follow
    A rule is input as "Sensor == Value; Reward/Punish"
    """

    def __init__(self, text):
        string = text.split(";")
        self.returns = string[1]
        string = string[0].split(" ")
        self.sensor = string[0]
        self.value = string[-1]


class Dog_Part:
    """
    A component of the dog. Something like a wheel or a sensor.
    """

    def __init__(self, coordinates, sensor, collision_type, colour):
        self.coordinates = coordinates
        self.sensor = sensor
        self.collision_type = collision_type
        self.colour = colour

        self.shape = pymunk.Poly(None, self.coordinates, radius=0.5)

    def get_vertices(self):
        vertices = []
        bx = self.shape.body.position[0]
        by = self.shape.body.position[1]
        for v in self.shape.get_vertices():
            vertices.append((v[0] + bx, v[1] + by))
        return vertices

    def draw(self):
        """
        draws the individual part
        """
        pygame.draw.polygon(screen, self.colour, self.get_vertices())


class Dog:
    """
    The dog simulated by the simulation.
    """

    def __init__(self, parts):
        # TODO Dog Stuff
        self.body = pymunk.Body(1, 1)
        self.body.position = (width / 2, height / 2)
        self.parts = []
        for part in parts:
            self.attach_part(part)
            self.parts.append(part)

    def attach_part(self, part):
        """
        Attaches a part to the dog
        """
        part.body = self.body
        self.parts.append(part)

    def add_to_sim(self, simulation):
        simulation.add(self.body)
        simulation.add_group(self.parts)

    def draw(self):
        """
        draws each individual part of the dog into the pygame window
        """
        for part in self.parts:
            part.draw()


class Object_Type:
    """
    An object type for the purposes of the simulation
    """

    def __init__(self, colour, alpha, collide, collision_type):
        self.colour = colour
        self.alpha = alpha
        self.collide = collide
        self.collision_type = collision_type


class Object_Instance:
    """
    An instance of an object type for the simulation
    """

    def __init__(self, type, size, position, simulation):
        # Instantiates the basic components of the object
        self.colour = type.colour
        self.alpha = type.alpha
        self.collide = type.collide
        self.collision = type.collision_type
        self.size = size
        self.position = position
        self.simulation = simulation

        # Handles the PyMunk parts of the object
        self.body = pymunk.Body(1, 0, pymunk.Body.STATIC)
        self.body.position = self.position
        self.shape = pymunk.Poly.create_box(self.body, (self.size, self.size), radius=1)
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
        pygame.draw.polygon(screen, self.colour, self.get_vertices())


class Simulation:
    """
    A simulation instance for the purpose of replicating the dogs movement, and visually displaying this
    to the user.
    """

    def __init__(self):
        self.space = pymunk.Space()
        self.collision_shapes = []
        self.simulation_objects = []
        self.set_boundaries()
        self.dog = None

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

    def add_group_shapes(self, objects):
        """
        Adds the shapes to the simulation
        """
        for obj in objects:
            self.space.add(obj.shape)

    def add(self, object):
        """
        Adds an individual object to the simulation
        """
        self.space.add(object)

    def step(self, time):
        """
        This steps the space for the time specified
        """
        self.space.step(time)

    def draw_simulation_objects(self):
        """
        This draws the shapes within the simulation into the pygame window
        """
        screen.fill([0, 90, 0])
        for object in self.simulation_objects:
            object.draw()

    

    def draw_dog(self):
        """
        draws the dog into the pygame window
        """
        if self.dog != None:
            self.dog.draw()

    def display_update(self):
        """
        updates the pygame window
        """
        self.draw_simulation_objects()
        self.draw_dog()
        pygame.display.update()


black = [0, 0, 0]

sim = Simulation()

brick = Object_Type([255, 255, 0], 255, True, 1)
sim.add_static_body(brick, 50, (360, 360))
sim.add_static_body(brick, 50, (40, 40))

chassis = Dog_Part([(5, 0), (15, 0), (15, 20), (5, 20)], False, 0, black)
left_wheel = Dog_Part([(0, 0), (5, 0), (5, 10), (0, 10)], False, 0, black)
right_wheel = Dog_Part([(15, 0), (20, 0), (20, 10), (15, 10)], False, 0, black)

dog_parts = [chassis, left_wheel, right_wheel]
dog = Dog(dog_parts)

while True:
    sim.step(0.01)
    sim.display_update()
