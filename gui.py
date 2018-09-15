from tkinter import *
import tkinter.ttk as tk



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

        """
        the object bit
        """
        self.object_frame_header = Frame(self.object_frame, width=400, height=30)
        self.object_frame_main = Canvas(self.object_frame, width=383, height=570, bg="#999999", scrollregion=(0, 0, 383, 1000))
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


#todo
#try having two loops, a loop for the menu, and then once that's handled go to the pygame window
#in the pygame one, also render a tk with a quit on it
#when you quit go back to settings
#stop buggery during the simulation

window = GUI_Window()
while True:
    window.root.update_idletasks()
    window.root.update()