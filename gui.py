from tkinter import *
import tkinter.ttk as tk


class Object_Interface:
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

        self.object_colour = Entry(self.colour_frame, textvariable=self.colour_var)
        self.collision_type = Entry(self.type_frame, textvariable=self.type_var)
        self.is_sensor = BooleanVar()
        self.object_type_is_sensor = Checkbutton(self.left_frame, text="Sensor", var=self.is_sensor)

    def pack_all(self):
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
    def __init__(self, gui):
        self.gui = gui
        self.frame = Frame(gui.rules_frame_main)
        self.entries_frame = Frame(self.frame)
        self.radio_frame = Frame(self.frame)

        self.object1_frame = Frame(self.entries_frame)
        self.object2_frame = Frame(self.entries_frame)

        self.object1_label = Label(self.object1_frame, text="Object 1", width=14, anchor=E)
        self.object2_label = Label(self.object2_frame, text="Object 2", width=14, anchor=E)

        self.object_1 = Entry(self.object1_frame)
        self.object_2 = Entry(self.object2_frame)

        self.output = IntVar()
        self.output.set(0)

        self.is_punish = Radiobutton(self.radio_frame, text="Punish", indicatoron=0, width=10, variable=self.output,
                                     value=0)
        self.is_reward = Radiobutton(self.radio_frame, text="Reward", indicatoron=0, width=10, variable=self.output,
                                     value=1)

    def pack_all(self):
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
        self.root = Tk()
        self.root.maxsize(height=700)
        self.root.title("Pyvlov's Dog - Settings")
        self.root.iconbitmap('favicon.ico')
        self.root.resizable(0, 0)
        self.has_quit = False
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        self.notebook = tk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=1)

        self.rule_frame = Frame(self.root, width=400, height=600)
        self.object_frame = Frame(self.root, width=400, height=600)
        self.settings_frame = Frame(self.root, width=400, height=600)

        self.notebook.add(self.rule_frame, text="Rules")
        self.notebook.add(self.object_frame, text="Objects")
        self.notebook.add(self.settings_frame, text="Simulator Settings")

        """
        the rules bit
        """
        self.rules = []

        self.rules_frame_header = Frame(self.rule_frame, width=400, height=30)
        self.rules_frame_main = Canvas(self.rule_frame, width=383, height=570, bg="#999999")
        self.add_rule_button = Button(self.rules_frame_header, text="New Rule", command=self.add_rule)
        self.delete_rule_button = Button(self.rules_frame_header, text="Delete Rule", command=self.remove_rule)
        self.rules_frame_scrollbar = Scrollbar(self.rule_frame)

        self.rules_frame_header.pack(fill=X)
        self.add_rule_button.pack(side=LEFT, padx=3)
        self.delete_rule_button.pack(side=LEFT, padx=3)
        self.rules_frame_main.pack_propagate(0)
        self.rules_frame_main.pack(side=LEFT, fill=BOTH)
        self.rules_frame_scrollbar.pack(side=RIGHT, fill=Y)
        self.rules_frame_main.configure(yscrollcommand=self.rules_frame_scrollbar.set)
        self.rules_frame_scrollbar.config(command=self.rules_frame_main.yview)
        """
        the object bit
        """

        self.objects = []

        self.object_frame_header = Frame(self.object_frame, width=400, height=30)
        self.object_frame_main = Canvas(self.object_frame, width=383, height=570, bg="#999999",
                                        scrollregion=(0, 0, 383, 1000))
        self.new_object_button = Button(self.object_frame_header, text="New Object", command=self.add_object)
        self.remove_object_button = Button(self.object_frame_header, text="Delete Object", command=self.remove_object)
        self.object_frame_scrollbar = Scrollbar(self.object_frame)

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
        the simulator settings bit
        """
        self.simulation_speed = Scale(self.settings_frame)

    def add_object(self):
        new_object_window = Object_Interface(self)
        self.objects.append(new_object_window)
        new_object_window.pack_all()

    def remove_object(self):
        del (self.objects[-1])
        self.object_frame_main.delete(ALL)
        for object in self.objects:
            object.pack_all()

    def add_rule(self):
        new_rule_window = Rule_Interface(self)
        self.rules.append(new_rule_window)
        new_rule_window.pack_all()

    def remove_rule(self):
        del (self.rules[-1])
        self.rules_frame_main.delete(ALL)
        for rule in self.rules:
            rule.pack_all()

    def quit(self):
        self.has_quit = True
        self.root.destroy()


class Running_Object_Window:
    def __init__(self, object, super_gui):
        self.super_gui = super_gui
        self.canvas = super_gui.object_frame
        self.frame = Frame(self.canvas)

        self.colour = object.colour_var.get()
        self.type = object.type_var.get()
        self.is_sensor = object.is_sensor.get()

        self.label_frame = Frame(self.frame)
        self.colour_label = Label(self.label_frame, text=("Colour: " + self.colour))
        self.type_label = Label(self.label_frame, text=("Object Type: " + self.type))
        self.is_sensor_label = Label(self.label_frame, text=("Sensor: " + str(self.is_sensor)))

        self.button_frame = Frame(self.frame)
        self.add_button = Button(self.button_frame, width=5, height=5, text="Add")
        self.clear_button = Button(self.button_frame, width=5, height=5, text="Clear")

    def pack_all(self):
        self.canvas.create_window(2, (self.super_gui.object_types.index(self)) * 95, width=379, height=93,
                                  window=self.frame, anchor=NW)
        self.label_frame.pack(side=LEFT)
        self.colour_label.pack(anchor=E)
        self.type_label.pack(anchor=E)
        self.is_sensor_label.pack(anchor=E)

        self.button_frame.pack(side=LEFT)
        self.add_button.pack(side=LEFT)
        self.clear_button.pack(side=LEFT)

    def queue_instance(self, size, position):
        self.super_gui.object_instances.append([self, size, position])

class Running_GUI:
    def __init__(self, old_gui):
        self.root = Tk()
        self.root.maxsize(height=700)
        self.root.title("Pyvlov's Dog - Settings")
        self.root.iconbitmap('favicon.ico')
        self.root.resizable(0, 0)
        self.has_quit = False
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.object_types = []
        self.object_frame = Canvas(self.root, width=383, height=570, bg="#999999", scrollregion=(0, 0, 383, 1000))
        self.object_instances = []

        self.object_frame.pack()

        for object in old_gui.objects:
            new_object = Running_Object_Window(object, self)
            self.object_types.append(new_object)
            new_object.pack_all()

    def quit(self):
        self.has_quit = True
        self.root.destroy()

    def get_object_list(self):
        return self.object_types
