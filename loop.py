import simulation as sm

black = [0, 0, 0]
brown = [90, 90, 30]
yellow = [255, 255, 0]

sim = sm.Simulation()

light = sm.Object_Type([255, 255, 0], 255, True, 1)
sim.add_static_body(light, 50, (640, 200))
sim.add_static_body(light, 50, (40, 40))

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
while True:
    wheel_values = sim.input_network()
    sim.step(0.01, wheel_values[0], wheel_values[1])
    sim.display_update()
