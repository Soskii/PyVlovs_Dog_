import simulation as sm

black = [0, 0, 0]
brown = [51, 51, 0]
yellow = [255, 255, 0]
red = [90, 0, 0]

sim = sm.Simulation()

light = sm.Object_Type(yellow, True, 1)
sim.add_static_body(light, 50, (640, 200))
sim.add_static_body(light, 50, (40, 40))

brick = sm.Object_Type(red, False, 4)
sim.add_static_body(brick, 75, (640, 300))

chassis = sm.Dog_Part([(0, 0), (50, 0), (50, 100), (0, 100)], (-25, -25), False, 0, brown)

left_wheel = sm.Dog_Part([(0, 0), (10, 0), (10, 30), (0, 30)], (-36, -20), False, 0, black, wheel="L")
right_wheel = sm.Dog_Part([(0, 0), (10, 0), (10, 30), (0, 30)], (26, -20), False, 0, black, wheel="R")
b_left_wheel = sm.Dog_Part([(0, 0), (10, 0), (10, 30), (0, 30)], (-36, 35), False, 0, black, wheel="L")
b_right_wheel = sm.Dog_Part([(0, 0), (10, 0), (10, 30), (0, 30)], (26, 35), False, 0, black, wheel="R")

ldr = sm.Dog_Part([(0, 0), (50, 0), (50, 6), (0, 6)], (-25, -35), True, 2, yellow)
ultra_sonic = sm.Dog_Part([(0, 0), (6, 0), (6, 40), (0, 40)], (-3, -65), True, 3, black)

dog_parts = [chassis, left_wheel, right_wheel, b_left_wheel, b_right_wheel, ldr, ultra_sonic]
sim.add_dog(dog_parts)

sim.add_collision_handler(2, 1, "punish")
sim.add_collision_handler(3, 4, "reward")

while True:
    wheel_values = sim.input_network()
    sim.step(0.01, wheel_values[0], wheel_values[1])
    sim.display_update()
