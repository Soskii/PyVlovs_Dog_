from tkinter import *
import tkinter.ttk as tk


class Object_Interface:
    def __init__(self, gui):
        self.frame = Frame(gui.object_frame_main)
        self.left_frame = Frame(self.frame, width=)

        self.object_type_colour = Entry()
        self.collision_type = Entry()
        self.object_type_is_sensor = Checkbutton()

        self.make_paintbrush = Button()
        self.clear_all = Button()



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
        self.rules_frame_header = Frame(self.rule_frame, width=400, height=30)
        self.rules_frame_main = Canvas(self.rule_frame, width=383, height=570, bg="#999999")
        self.add_rule_button = Button(self.rules_frame_header, text="New Rule")
        self.delete_rule_button = Button(self.rules_frame_header, text="Delete Rule")
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

        objects = []

        self.object_frame_header = Frame(self.object_frame, width=400, height=30)
        self.object_frame_main = Canvas(self.object_frame, width=383, height=570, bg="#999999",
                                        scrollregion=(0, 0, 383, 1000))
        self.new_object_button = Button(self.object_frame_header, text="New Object")
        self.remove_object_button = Button(self.object_frame_header, text="Delete Object")
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


# todo
# try having two loops, a loop for the menu, and then once that's handled go to the pygame window
# in the pygame one, also render a tk with a quit on it
# when you quit go back to settings
# stop buggery during the simulation

window = GUI_Window()
while True:
    window.root.update_idletasks()
    window.root.update()
