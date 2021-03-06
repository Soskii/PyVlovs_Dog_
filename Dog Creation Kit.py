from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import os
import ast

root = Tk()
root.minsize(height=600, width=800)
root.resizable(0, 0)
root.title("Pyvlov's Dog - Dog Generator")
root.iconbitmap('assets/favicon.ico')

#####objects#####

menu_frame = Frame(root)

parts = []


class Wid:
    """
    A class used for handling the widgets in the part list.
    """

    def __init__(self, name, widget, parent, var=None, preset=None):
        self.name = name  # The widgets name, used for a label.
        self.widgetn = widget  # The type of widget.
        self.frame = Frame(parent, height=20, width=373)
        # Handles both ENTRY and CHECK widget types.
        if self.widgetn == "entry":
            self.widget = Entry(self.frame, width=45)
            if preset != None:
                self.widget.insert(END, preset)
        if self.widgetn == "check":
            self.var = var
            if preset != None:
                self.var.set(int(preset))
            self.widget = Checkbutton(self.frame, variable=var)
        # Creates a label for the widget, inside the frame
        self.label = Label(self.frame, text=self.name, width=12, anchor=E)

    def pack(self):
        # Packs all the components of the widget
        self.frame.pack(fill=X, pady=1, padx=3)
        self.label.pack(side=LEFT)
        self.widget.pack(side=LEFT, fill=X)

    def get(self):
        # Returns the content of the widget the user has entered.
        return self.widget.get() if self.widgetn == "entry" else self.var.get()


class Part:
    """
    The structure that handles a dog component in the kit.

    """

    # Presets exist so that the saves are available.
    def __init__(self, pre_shape_vertices=None, pre_displacement=None, pre_sensor=None, pre_collision_type=None,
                 pre_colour=None,
                 pre_wheel=None):
        self.frame = Frame(parts_window)
        self.shape_vertices = Wid("Shape Vertices", "entry", self.frame, preset=pre_shape_vertices)
        self.displacement = Wid("Displacement", "entry", self.frame, preset=pre_displacement)

        self.sensor_var = IntVar()
        self.sensor = Wid("Sensor", "check", self.frame, preset=pre_sensor, var=self.sensor_var)
        self.sensor.var = self.sensor_var

        self.collision_type = Wid("Collision Type", "entry", self.frame, preset=pre_collision_type)
        self.colour = Wid("Colour", "entry", self.frame, preset=pre_colour)
        self.wheel = Wid("Wheel", "entry", self.frame, preset=pre_wheel)

    def draw(self):
        # Like a print statement for the part menu.
        parts_window.create_window(2, (parts.index(self)) * 166, width=379, height=165, window=self.frame, anchor=NW)
        self.shape_vertices.pack()
        self.displacement.pack()
        self.sensor.pack()
        self.collision_type.pack()
        self.colour.pack()
        self.wheel.pack()
        parts_window.configure(scrollregion=(0, 0, 383, len(parts) * 166))


def part_add():
    # Adds another part to the list.
    parts.append(Part())
    parts[-1].draw()


def part_rem():
    # Removes the last part in the list.
    parts_window.delete(ALL)
    del (parts[-1])
    for obj in parts:
        obj.draw()


def hex_to_dec(hex_code):
    """
    Converts from a 6 digit hexadecimal value with a leading hash to a list of 3 decimal values.

    """
    conversion_dict = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15,
                       "a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15}
    hex_code = hex_code[1:]  # Removes the #
    # Gets the rgb values.
    r_h_value = hex_code[:2]
    g_h_value = hex_code[2:4]
    b_h_value = hex_code[4:6]
    # Converts it into a list
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
    return tuple(dec_rgb)


def img_gen():
    """
    Generates an image using PIL of the dog.
    """
    loc = location.get()
    global im
    # Creates an image in the correct format.
    im = Image.new("RGBA", (383, 570), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    for part in parts:
        c_g = hex_to_dec(part.colour.get())
        vertices = ast.literal_eval(part.shape_vertices.get())
        displacement = ast.literal_eval(part.displacement.get())
        displaced_vertices = []
        dx, dy = int(displacement[0]), int(displacement[1])
        for point in vertices:
            new_x = point[0] + dx + 200
            new_y = point[1] + dy + 275
            displaced_vertices.append((new_x, new_y))

        # Draws a polygon in the image that is in the correct position/colour.
        draw.polygon(displaced_vertices, c_g)
        global ph
        ph = ImageTk.PhotoImage(im)
        canvas.create_image(0, 0, image=ph, anchor=NW)
    im.save(loc + "\\img.png")
    # Crops the image.
    cropco = im.getbbox()
    if cropco != None:
        cropped = im.crop(cropco)
        cropped.save(loc + "\\sim_dog.png")




def exporting():
    """
    Acts as the save feature of the program. Copies the content of the dog into a file.
    """
    global im
    loc = location.get()
    if not os.path.exists(loc):
        os.mkdir(loc)
    file = open(loc + "\data.txt", "w+")
    file.truncate(0)
    for part in parts:
        file.write("#start#\n")
        file.write(part.shape_vertices.get() + "\n")
        file.write(part.displacement.get() + "\n")
        file.write(str(part.sensor.get()) + "\n")
        file.write(part.collision_type.get() + "\n")
        file.write(part.colour.get() + "\n")
        file.write(part.wheel.get() + "\n")
        file.write("#end#\n")


def importing():
    """
    Imports an existing save into the program for editing.
    """
    loc = location.get()
    file = open(loc + "\data.txt", "r")
    global parts
    parts = []
    text = []
    for line in file:
        text.append(line.strip())
    parts_window.delete(ALL)
    for dat in range(len(text)):
        if text[dat] == "#start#":
            parts.append(Part(text[dat + 1], text[dat + 2], text[dat + 3], text[dat + 4], text[dat + 5], text[dat + 6]))
            parts[-1].draw()
    img_gen()

"""
Packs in the content of the window.
"""
menu_frame.pack(side=LEFT)
top_omenu = Frame(menu_frame, width=400, height=30, bg="#777777")
parts_window = Canvas(menu_frame, width=383, height=570, bg="#999999", scrollregion=(0, 0, 383, 1000))
parts_window.pack_propagate(0)
createo_button = Button(top_omenu, text="New Part", command=part_add)
removeo_button = Button(top_omenu, text="Delete Part", command=part_rem)
update = Button(top_omenu, text="Update", command=img_gen)
scrollo = Scrollbar(menu_frame)

top_omenu.pack(fill=X)
createo_button.pack(side=LEFT, padx=3, pady=1)
removeo_button.pack(side=LEFT, padx=3, pady=1)
update.pack(side=LEFT, padx=3, pady=1)
parts_window.pack(side=LEFT)
scrollo.config(command=parts_window.yview)
scrollo.pack(side=RIGHT, fill=Y)
parts_window.configure(yscrollcommand=scrollo.set)
parts_window.configure(yscrollincrement="2")

"""
Handles the canvas in the window.
"""
global ph

r_frame = Frame(root, width=400, height=600)
canvas = Canvas(r_frame, width=400, height=550, bg="#777777", highlightthickness=1)

buttons = Frame(r_frame, width=400, height=50, bg="#999999")
buttons.pack_propagate(0)
v = StringVar(root, value="saves\\")
location = Entry(buttons, textvariable=v)
export = Button(buttons, text="Export", width=27, command=exporting)
importer = Button(buttons, text="Import", width=27, command=importing)

r_frame.pack(side=LEFT)
canvas.pack()
buttons.pack()
location.pack(fill=X)
export.pack(side=LEFT, fill=Y)
importer.pack(side=LEFT, fill=Y)

mainloop()
