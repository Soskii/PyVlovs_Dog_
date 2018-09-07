from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import os
import ast

# TODO add options for centre of dog and

root = Tk()
root.minsize(height=600, width=800)
root.resizable(0, 0)
root.title("Pyvlov's Dog - Dog Generator")
root.iconbitmap('favicon.ico')

#####objects#####

menu_frame = Frame(root)

parts = []


class Wid:
    def __init__(self, name, widget, parent, var=None, preset=None):
        self.name = name
        self.widgetn = widget
        self.frame = Frame(parent, height=20, width=383)
        if self.widgetn == "entry":
            self.widget = Entry(self.frame, width=49)
            if preset != None:
                self.widget.insert(END, preset)
        if self.widgetn == "check":
            self.var = var
            if preset != None:
                self.var.set(int(preset))
            self.widget = Checkbutton(self.frame, variable=var)
        self.label = Label(self.frame, text=self.name, width=10, anchor=E)

    def pack(self):
        self.frame.pack(fill=X, pady=1)
        self.label.pack(side=LEFT, fill=X)
        self.widget.pack(side=LEFT, fill=X)

    def get(self):
        return self.widget.get() if self.widgetn == "entry" else self.var.get()


class Part:
    def __init__(self, pre_name=None, pre_colour=None, pre_vertices=None, pre_input_link=None, pre_settings=None,
                 pre_collide=None,
                 pre_wheel=None):
        # name, colour, vertices, wheel, collide, detects
        # Labels
        self.frame = Frame(parts_window)
        # self.l_frame.pack_propagate(0)

        self.name = Wid("Name", "entry", self.frame, preset=pre_name)
        self.colour = Wid("Colour", "entry", self.frame, preset=pre_colour)
        self.vertices = Wid("Vertices", "entry", self.frame, preset=pre_vertices)
        self.input_link = Wid("Sensor Type", "entry", self.frame, preset=pre_input_link)
        self.settings = Wid("Settings", "entry", self.frame, preset=pre_settings)

        self.var = IntVar()
        self.collide = Wid("Collide", "check", self.frame, var=self.var, preset=pre_collide)
        self.collide.var = self.var

        self.wvar = IntVar()
        self.wheel = Wid("Wheel", "check", self.frame, var=self.wvar, preset=pre_wheel)
        self.wheel.var = self.wvar

    def draw(self):
        parts_window.create_window(2, (parts.index(self)) * 166, width=379, height=165, window=self.frame, anchor=NW)
        self.name.pack()
        self.colour.pack()
        self.vertices.pack()
        self.input_link.pack()
        self.settings.pack()
        self.collide.pack()
        self.wheel.pack()
        parts_window.configure(scrollregion=(0, 0, 383, len(parts) * 166))


def part_add():
    parts.append(Part())
    parts[-1].draw()


def part_rem():
    parts_window.delete(ALL)
    del (parts[-1])
    for obj in parts:
        obj.draw()

    # parts_window.configure(scrollregion=(0, 0, 383, 500 if len(parts) < 6 else len(parts) * 100))


def img_gen():
    loc = location.get()
    global im
    im = Image.new("RGBA", (383, 570), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    for part in parts:
        c_g = part.colour.get()
        try:
            if len(c_g) != 9:
                raise Exception
            colour = (int(c_g[0:3]), int(c_g[3:6]), int(c_g[6:9]))
            if any(x not in range(0, 256) for x in colour):
                raise Exception
        except Exception:
            colour = (000, 000, 000)
        vertices = ast.literal_eval(part.vertices.get())
        draw.polygon(vertices, colour)
        global ph
        ph = ImageTk.PhotoImage(im)
        canvas.create_image(0, 0, image=ph, anchor=NW)
    im.save(loc + "\\img.png")
    cropco = im.getbbox()
    if cropco != None:
        print(cropco)
        cropped = im.crop(cropco)
        cropped.save(loc + "\\sim_dog.png")


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

#####canvas#####
global ph


def exporting():
    global im
    loc = location.get()
    if not os.path.exists(loc):
        os.mkdir(loc)
    file = open(loc + "\data.txt", "w+")
    file.truncate(0)
    boundingbox = im.getbbox()
    file.write(str(boundingbox) + "\n")
    for part in parts:
        file.write("#start#\n")
        file.write(part.name.get() + "\n")
        file.write(part.colour.get() + "\n")
        file.write(part.vertices.get() + "\n")
        file.write(part.input_link.get() + "\n")
        file.write(part.settings.get() + "\n")
        file.write(str(part.collide.get()) + "\n")
        file.write(str(part.wheel.get()) + "\n")
        file.write("#end#\n")
        ### TODO include settings entry for wheel size and others


def importing():
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
            parts.append(Part(text[dat + 1], text[dat + 2], text[dat + 3], text[dat + 4], text[dat + 5], text[dat + 6],
                              text[dat + 7]))
            parts[-1].draw()
    img_gen()
    print(parts)


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
