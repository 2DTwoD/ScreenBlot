import  tkinter as tk
from enum import Enum


class ShapeType(Enum):
    NONE = 0,
    PENCIL = 1,
    RECTANGLE = 2,
    OVAL = 3,
    POLYGON = 4,
    TEXT = 5,

class InstrumentPanel(tk.Frame):
    def __init__(self, parent, root, transparent_color, clear_action, undo_action):
        tk.Frame.__init__(self, parent, background=transparent_color)

        self.type = ShapeType.POLYGON

        close = tk.Button(self, text='X', command=root.destroy, width=3, font='Courier 10 bold')
        clear = tk.Button(self, text='C', command=clear_action, width=3, font='Courier 10 bold')
        undo = tk.Button(self, text='<-', command=undo_action, width=3, font='Courier 10 bold')

        none_button = tk.Button(self, text='.', command=lambda: self.setType(ShapeType.NONE), width=3, font='Courier 10 bold')
        pencil_button = tk.Button(self, text='~', command=lambda: self.setType(ShapeType.PENCIL), width=3, font='Courier 10 bold')
        rect_button = tk.Button(self, text='□', command=lambda: self.setType(ShapeType.RECTANGLE), width=3, font='Courier 10 bold')
        oval_button = tk.Button(self, text='O', command=lambda: self.setType(ShapeType.OVAL), width=3, font='Courier 10 bold')
        polygon_button = tk.Button(self, text='L', command=lambda: self.setType(ShapeType.POLYGON), width=3, font='Courier 10 bold')
        text_button = tk.Button(self, text='T', command=lambda: self.setType(ShapeType.TEXT), width=3, font='Courier 10 bold')

        close.pack(anchor=tk.NE)
        clear.pack(anchor=tk.NE)
        undo.pack(anchor=tk.NE)

        none_button.pack(anchor=tk.NE)
        pencil_button.pack(anchor=tk.NE)
        rect_button.pack(anchor=tk.NE)
        oval_button.pack(anchor=tk.NE)
        polygon_button.pack(anchor=tk.NE)
        text_button.pack(anchor=tk.NE)

    def bind_frame(self, sequence=None, func=None, add=None):
        for child in self.winfo_children():
            child.bind(sequence, func, add)

    def setType(self, new_type):
        self.type = new_type
