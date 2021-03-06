import simulation as sm
import gui
import ast

"""
A placeholder create dog function, to be made customisable in the gui
"""


def convert(string):
    return ast.literal_eval(string)


def create_dog(directory):
    """
    Reads in the allocated dog save file, so as to commit it to the simulation
    """
    parts = []
    text = open(directory + "\\data.txt").read()
    text_parts = text.split("#end#")
    del text_parts[-1]
    for part in text_parts:
        # Reads each part in the file, appending them all into the dog object
        att = part.strip().split("\n")
        parts.append(
            sm.Dog_Part(convert(att[1]), convert(att[2]), convert(att[3]), convert(att[4]), att[5], wheel=att[6]))
    return parts


while True:
    window = gui.GUI_Window()
    while not window.has_quit:
        # Updates the dogs location and network location until the user closes the window.
        dog_location = window.dog_location_entry.get()
        network_location = window.network_location_entry.get()
        window.root.update_idletasks()
        window.root.update()
    if window.exiting:
        # Triggers when the user has hit the quit button
        break
    # Instantiates the simulation and the complementary GUI window.
    run_menu = gui.Running_GUI(window)
    sim = sm.Simulation()
    sim.set_network(network_location)
    sim.add_dog(create_dog(dog_location))
    sim_speed = float(window.sim_speed_var.get())
    for rule in window.rules:
        # Converts the GUI rules into collision handlers.
        obj_1, obj_2, outcome = int(rule.first_obj.get()), int(rule.second_obj.get()), rule.output.get()
        sim.add_collision_handler(obj_1, obj_2, outcome)
    while not sim.has_quit and not run_menu.has_quit:
        # While the user hasn't closed the simulation keep stepping through it.
        run_menu.update_gui()
        for click in sim.current_clicks:
            # Converts the list of click locations into objects of the current brush's type.
            if run_menu.active_brush != None:
                sim.add_static_body(run_menu.active_brush, run_menu.active_brush.slider.get(), click)
        # Clears the click locations
        sim.current_clicks = []
        # Steps the simulation
        sim.step(sim_speed)

        run_menu.new_object_instances = []
        sim.display_update(True)
        sim.event_queue()
        # Resets feedback for next step
        sim.punish, sim.reward = False, False
        if sim.has_quit:
            run_menu.quit()
    if not sim.has_quit:
        sim.quit()
