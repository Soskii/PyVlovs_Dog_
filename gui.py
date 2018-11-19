from tkinter import *
import tkinter.ttk as tk

"""
For those unfamiliar with Tk

A frame is a box, similar to a DIV in html, for formatting
A label is a text object
Pack puts an object into its frame
"""


class Object_Interface:
    """
    The object handling the window created when the user adds an object
    """

    def __init__(self, gui):
        self.gui = gui
        self.instances = []
        self.frame = Frame(gui.object_frame_main)
        self.left_frame = Frame(self.frame)
        self.right_frame = Frame(self.frame)

        self.colour_frame = Frame(self.left_frame)
        self.type_frame = Frame(self.left_frame)

        self.object_colour_label = Label(self.colour_frame, text="Object Colour", width=14, anchor=E)
        self.object_type_label = Label(self.type_frame, text="Object Type", width=14, anchor=E)

        self.colour_var = StringVar()
        self.type_var = StringVar()

        # colour entered in 6 digit hex with leading hash "#999999"
        self.object_colour = Entry(self.colour_frame, textvariable=self.colour_var)
        self.collision_type = Entry(self.type_frame, textvariable=self.type_var)
        self.is_sensor = BooleanVar()
        self.object_type_is_sensor = Checkbutton(self.left_frame, text="Sensor", var=self.is_sensor)

    def pack_all(self):
        """
        the equivalent of a print function for this. Puts the object window into the frame so the user can interact with it
        """
        self.gui.object_frame_main.create_window(2, (self.gui.objects.index(self)) * 95, width=379, height=93,
                                                 window=self.frame, anchor=NW)
        self.left_frame.pack(side=LEFT)
        self.right_frame.pack(side=LEFT, padx=10)

        self.colour_frame.pack(pady=2)
        self.type_frame.pack(pady=2)

        self.object_colour_label.pack(side=LEFT)
        self.object_type_label.pack(side=LEFT)

        self.object_colour.pack()
        self.collision_type.pack()
        self.object_type_is_sensor.pack(side=TOP, fill=X)


class Rule_Interface:
    """
    The same as the object interface above, but for rules instead
    """

    def __init__(self, gui):
        self.gui = gui
        self.frame = Frame(gui.rules_frame_main)
        self.entries_frame = Frame(self.frame)
        self.radio_frame = Frame(self.frame)

        self.object1_frame = Frame(self.entries_frame)
        self.object2_frame = Frame(self.entries_frame)

        self.object1_label = Label(self.object1_frame, text="Object 1", width=14, anchor=E)
        self.object2_label = Label(self.object2_frame, text="Object 2", width=14, anchor=E)

        self.first_obj = StringVar()
        self.second_obj = StringVar()

        self.object_1 = Entry(self.object1_frame, textvariable=self.first_obj)
        self.object_2 = Entry(self.object2_frame, textvariable=self.second_obj)

        self.output = IntVar()
        self.output.set(0)

        self.is_punish = Radiobutton(self.radio_frame, text="Punish", indicatoron=0, width=10, variable=self.output,
                                     value=0)
        self.is_reward = Radiobutton(self.radio_frame, text="Reward", indicatoron=0, width=10, variable=self.output,
                                     value=1)

    def pack_all(self):
        """
        packs the rule into the gui
        """
        self.gui.rules_frame_main.create_window(2, (self.gui.rules.index(self)) * 95, width=379, height=93,
                                                window=self.frame, anchor=NW)
        self.entries_frame.pack(side=LEFT)
        self.object1_frame.pack()
        self.object2_frame.pack()
        self.object1_label.pack(side=LEFT)
        self.object2_label.pack(side=LEFT)
        self.object_1.pack(side=LEFT)
        self.object_2.pack(side=LEFT)

        self.radio_frame.pack(pady=20)
        self.is_punish.pack()
        self.is_reward.pack()


class GUI_Window:
    """
    the gui window object
    """

    def __init__(self):
        """
        Initialises the window
        """
        self.root = Tk()
        self.root.maxsize(height=700)
        self.root.title("Pyvlov's Dog - Settings")
        self.root.iconbitmap('assets/favicon.ico')
        self.root.resizable(0, 0)
        self.has_quit = False
        self.exiting = False
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        """
        The notebook allows for tabs
        """
        self.notebook = tk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=1)

        """
        The frames displayed on the notebook as each tab
        """
        self.readme_frame = Frame(self.root, width=400, height=600)
        self.object_frame = Frame(self.root, width=400, height=600)
        self.rule_frame = Frame(self.root, width=400, height=600)
        self.settings_frame = Frame(self.root, width=400, height=600)

        self.notebook.add(self.readme_frame, text="ReadMe")
        self.notebook.add(self.object_frame, text="Objects")
        self.notebook.add(self.rule_frame, text="Rules")
        self.notebook.add(self.settings_frame, text="Simulator Settings")


        """
        The readme
        """
        self.readme_container = Frame(self.readme_frame, width=383, height=570)
        self.readme = Text(self.readme_container, wrap=WORD)

        self.readme_text = open("readme.md").read()

        self.readme_container.pack(pady=10)
        self.readme_container.pack_propagate(0)
        self.readme.pack(expand=True, fill=BOTH)
        self.readme.insert(END, self.readme_text)
        self.readme.config(state=DISABLED)


        """
        the object bit
        """

        self.objects = []

        """
        puts together the object window
        """

        self.object_frame_header = Frame(self.object_frame, width=400, height=30)
        self.object_frame_main = Canvas(self.object_frame, width=383, height=570, bg="#999999",
                                        scrollregion=(0, 0, 383, 1000))
        self.new_object_button = Button(self.object_frame_header, text="New Object", command=self.add_object)
        self.remove_object_button = Button(self.object_frame_header, text="Delete Object", command=self.remove_object)
        self.object_frame_scrollbar = Scrollbar(self.object_frame)

        """
        
        """

        self.object_frame_main.pack_propagate(0)
        self.object_frame_header.pack(fill=X)
        self.new_object_button.pack(side=LEFT, padx=3)
        self.remove_object_button.pack(side=LEFT, padx=3)
        self.object_frame_main.pack(side=LEFT)
        self.object_frame_scrollbar.config(command=self.object_frame_main.yview)
        self.object_frame_scrollbar.pack(side=RIGHT, fill=Y)
        self.object_frame_main.configure(yscrollcommand=self.object_frame_scrollbar.set)
        self.object_frame_main.configure(yscrollincrement="2")

        """
        the rules bit
        """
        self.rules = []

        """
        Putting together the rules window
        """
        self.rules_frame_header = Frame(self.rule_frame, width=400, height=30)
        self.rules_frame_main = Canvas(self.rule_frame, width=383, height=570, bg="#999999")
        self.add_rule_button = Button(self.rules_frame_header, text="New Rule", command=self.add_rule)
        self.delete_rule_button = Button(self.rules_frame_header, text="Delete Rule", command=self.remove_rule)
        self.rules_frame_scrollbar = Scrollbar(self.rule_frame)

        """
        Packing it all into the gui window
        """

        self.rules_frame_header.pack(fill=X)
        self.add_rule_button.pack(side=LEFT, padx=3)
        self.delete_rule_button.pack(side=LEFT, padx=3)
        self.rules_frame_main.pack_propagate(0)
        self.rules_frame_main.pack(side=LEFT, fill=BOTH)
        self.rules_frame_scrollbar.pack(side=RIGHT, fill=Y)
        self.rules_frame_main.configure(yscrollcommand=self.rules_frame_scrollbar.set)
        self.rules_frame_scrollbar.config(command=self.rules_frame_main.yview)

        """
        the simulator settings bit
        """
        self.sim_speed_frame = Frame(self.settings_frame)
        self.sim_speed_label = Label(self.sim_speed_frame, text="Simulation Speed")
        self.sim_speed_var = StringVar()
        self.sim_speed = Scale(self.sim_speed_frame, orient=HORIZONTAL, variable=self.sim_speed_var, from_=0.01, to=1,
                               resolution=0.01)

        self.dog_location_frame = Frame(self.settings_frame)
        self.dog_location_entry = Entry(self.dog_location_frame, width=40)
        self.dog_location_entry.insert(END, "saves\\Default")
        self.dog_location_label = Label(self.dog_location_frame, text="Dog File Path", width=15, anchor=E)

        self.network_location_frame = Frame(self.settings_frame)
        self.network_location_entry = Entry(self.network_location_frame, width=40)
        self.network_location_entry.insert(END, "networks\\placeholder_network.py")
        self.network_location_label = Label(self.network_location_frame, text="Network File Path", width=15, anchor=E)

        self.quit_button = Button(self.settings_frame, text="Quit", command=self.exit, width=20, bg="#aa0000",
                                  fg="#ffffff")

        self.sim_speed_frame.pack()
        self.sim_speed_label.pack(side=LEFT)
        self.sim_speed.pack(side=LEFT)

        self.dog_location_frame.pack(fill=X, padx=5)
        self.dog_location_label.pack(side=LEFT)
        self.dog_location_entry.pack(side=LEFT, fill=X)

        self.network_location_frame.pack(fill=X, padx=5)
        self.network_location_label.pack(side=LEFT)
        self.network_location_entry.pack(side=LEFT, fill=X)
        self.quit_button.pack(side=BOTTOM, pady=20)

    def add_object(self):
        # Add an object to the object window
        new_object_window = Object_Interface(self)
        self.objects.append(new_object_window)
        new_object_window.pack_all()

    def remove_object(self):
        # Removes the most recent object
        del (self.objects[-1])
        self.object_frame_main.delete(ALL)
        for object in self.objects:
            object.pack_all()

    def add_rule(self):
        # Adds a rule into the gui for editing.
        new_rule_window = Rule_Interface(self)
        self.rules.append(new_rule_window)
        new_rule_window.pack_all()

    def remove_rule(self):
        # Removes the most recent rule in the list.
        del (self.rules[-1])
        self.rules_frame_main.delete(ALL)
        for rule in self.rules:
            rule.pack_all()

    def quit(self):
        # Triggers with the close of the GUI window, not the manual exit button.
        self.has_quit = True
        self.root.destroy()

    def exit(self):
        # Triggers on the exit button that actually closes the window.
        self.exiting = True
        self.quit()


class Object_Type:
    """
    An object type for the purposes of the simulation
    """

    def __init__(self, colour, collide, collision_type):
        self.colour = colour
        self.collide = int(collide)
        self.collision_type = int(collision_type)


class Running_Object_Window:
    """
    The object handling a given object in the runtime GUI.
    """

    def __init__(self, object, super_gui):
        self.super_gui = super_gui
        self.canvas = super_gui.object_frame
        self.frame = Frame(self.canvas)

        self.colour_text = object.colour_var.get()
        self.colour_rgb = hex_to_dec(self.colour_text)

        self.type = object.type_var.get()
        self.is_sensor = object.is_sensor.get()

        self.slider = Scale(self.frame, orient=HORIZONTAL, label="Size", to=100)

        self.label_frame = Frame(self.frame)
        self.colour_label = Label(self.label_frame, text=("Colour: " + self.colour_text))
        self.type_label = Label(self.label_frame, text=("Object Type: " + self.type))
        self.is_sensor_label = Label(self.label_frame, text=("Sensor: " + str(self.is_sensor)))

        self.colour_display = Frame(self.frame, height=40, width=40, bg=self.colour_text)

        self.button_frame = Frame(self.frame)
        self.add_button = Button(self.button_frame, width=10, height=5, text="Add", command=self.set_active)

        self.template = Object_Type(self.colour_rgb, self.is_sensor, self.type)

    def pack_all(self):
        self.canvas.create_window(2, (self.super_gui.object_types.index(self)) * 95, width=379, height=93,
                                  window=self.frame, anchor=NW)
        self.label_frame.pack(side=LEFT, padx=10)
        self.colour_label.pack(anchor=E)
        self.type_label.pack(anchor=E)
        self.is_sensor_label.pack(anchor=E)

        self.colour_display.pack(side=LEFT, padx=40)
        self.slider.pack()

        self.button_frame.pack(side=RIGHT)
        self.add_button.pack(side=LEFT)

    def set_active(self):
        # Sets the active brush for the simulation, for object creation.
        self.super_gui.active_brush = self


class Running_GUI:
    """
    The object handling the full runtime GUI
    """

    def __init__(self, old_gui):
        self.root = Tk()
        self.root.maxsize(height=700)
        self.root.title("Pyvlov's Dog - Settings")
        self.root.iconbitmap('assets/favicon.ico')
        self.root.resizable(0, 0)
        self.has_quit = False
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.object_types = []
        self.object_frame = Canvas(self.root, width=383, height=570, bg="#999999", scrollregion=(0, 0, 383, 1000))
        self.object_instances = []
        self.new_object_instances = []
        self.active_brush = None

        self.object_frame.pack()

        for object in old_gui.objects:
            # Converts the GUI objects for use in the runtime window.
            new_object = Running_Object_Window(object, self)
            self.object_types.append(new_object)
            new_object.pack_all()

    def update_gui(self):
        # Used for keeping the gui updated.
        self.root.update_idletasks()
        self.root.update()

    def quit(self):
        self.has_quit = True
        self.root.destroy()

    def get_object_list(self):
        return self.object_types


def hex_to_dec(hex_code):
    """
    Converts from a 6 digit hexadecimal value with a leading hash to a list of 3 decimal values.

    """
    conversion_dict = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15,
                       "a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
    hex_code = hex_code[1:]
    r_h_value = hex_code[:2]
    g_h_value = hex_code[2:4]
    b_h_value = hex_code[4:6]
    hex_rgb = [r_h_value, g_h_value, b_h_value]
    dec_rgb = []
    for hex in hex_rgb:
        dec_value = 0
        for integer, value in enumerate(hex):
            if value in conversion_dict:
                value = conversion_dict[value]
            else:
                value = int(value)
            dec_value += value * (16 ** (1 - integer))
        dec_rgb.append(dec_value)
    return dec_rgb
