import operator
import tkinter as tk
from enum import Enum

from autosize_entry import AutosizeEntry


class ShapeType(Enum):
    LINE = 0,
    RECTANGLE = 1,
    OVAL = 2,
    POLYGON = 3,
    TEXT = 4,


class RootCanvas(tk.Canvas):
    def __init__(self, root, transparent_color):
        tk.Canvas.__init__(self, root, bg=transparent_color, bd=0, highlightthickness=0)
        close = tk.Button(self, text='X', command=root.destroy, width=3)
        close.bind('<Button-1>', lambda e: self.menu_busy_action())
        clear = tk.Button(self, text='C', command=self.clear_action, width=3)
        clear.bind('<Button-1>', lambda e: self.menu_busy_action())
        undo = tk.Button(self, text='<--', command=self.undo_action, width=3)
        undo.bind('<Button-1>', lambda e: self.menu_busy_action())

        self.transparent_color = transparent_color
        self.bind("<<Screen_lmouse_down>>", lambda e: self.after(1, self.lmouse_down_action, e.x, e.y))
        self.bind("<<Screen_lmouse_up>>", lambda e: self.after(1, self.lmouse_up_action, e.x, e.y))
        self.bind("<<Screen_mouse_move>>", lambda e: self.after(1, self.mouse_move_action, e.x, e.y))
        self.bind("<<Screen_rmouse_down>>", lambda e: self.after(1, self.rmouse_down_action, e.x, e.y))

        close.pack(anchor=tk.NE)
        clear.pack(anchor=tk.NE)
        undo.pack(anchor=tk.NE)

        self.type = ShapeType.POLYGON

        self.entry = None
        self.shape_id = None

        self.mouse_down = False
        self.start_click_drawing = False
        self.menu_clicked = False

        self.coordinates = []

        self.shape_for_moving = None
        self.move_shift_x = 0
        self.move_shift_y = 0

    def lmouse_down_action(self, x=0, y=0):
        if self.menu_clicked:
            self.menu_clicked = False
            return
        self.mouse_down = True
        self.coordinates.append((x, y))
        if self.shape_for_moving is None:
            self.start_click_drawing = self.type == ShapeType.POLYGON
            if self.type == ShapeType.TEXT:
                self.draw_shape()

    def mouse_move_action(self, x=0, y=0):
        if self.shape_for_moving is not None:
            self.coordinates.append((x, y))
            self.move(self.shape_for_moving, *self.get_coords_increment())
        elif self.type == ShapeType.TEXT:
            return
        elif self.mouse_down or self.start_click_drawing:
            self.draw_shape(x, y)

    def lmouse_up_action(self, x=0, y=0):
        self.mouse_down = False
        if self.type == ShapeType.POLYGON:
            if self.shape_for_moving is not None:
                self.coordinates.clear()
            self.shape_for_moving = None
            return
        self.end_drawing()

    def rmouse_down_action(self, x=0, y=0):
        if self.start_click_drawing:
            self.end_drawing()
            self.start_click_drawing = False

    def draw_shape(self, x=0, y=0):
        if self.shape_id is not None:
            self.delete(self.shape_id)
        match self.type:
            case ShapeType.LINE:
                self.coordinates.append((x, y))
                self.shape_id = self.create_line(self.coordinates, width=3, fill='white')
                # self.shape_id = self.create_polygon(*self.coordinates, x, y, width=3, outline='white', fill='red')
            case ShapeType.RECTANGLE:
                self.shape_id = self.create_rectangle(*self.coordinates, x, y, width=3, outline='white')
            case ShapeType.OVAL:
                self.shape_id = self.create_oval(*self.coordinates, x, y, width=3, outline='white')
            case ShapeType.POLYGON:
                self.shape_id = self.create_polygon(*self.coordinates, x, y, width=3, outline='white', fill='red')
            case ShapeType.TEXT:
                self.entry = AutosizeEntry(self, font='Courier 20 bold', bg='white', fg='black')
                self.shape_id = self.create_window(self.get_start_coords(), window=self.entry)

    def end_drawing(self):
        self.coordinates.clear()
        self.shape_for_moving = None
        if self.shape_id is None:
            return
        tmp_shape_id = self.shape_id
        if self.type == ShapeType.TEXT and self.entry is not None:
            self.entry.bind('<Button-1>', lambda e: self.shape_click_action(tmp_shape_id))
            self.entry.bind('<Button-3>', lambda e: self.delete(tmp_shape_id))
        else:
            self.tag_bind(self.shape_id, '<Button-1>', lambda e: self.shape_click_action(tmp_shape_id))
            self.tag_bind(self.shape_id, '<Button-3>', lambda e: self.delete(tmp_shape_id))

        self.shape_id = None
        self.entry = None

    def shape_click_action(self, shape_id):
        self.shape_for_moving = shape_id
        self.start_click_drawing = False

    def undo_action(self):
        self.rmouse_down_action()
        if len(self.find_all()) > 0:
            self.delete(self.find_all()[-1])

    def clear_action(self):
        self.rmouse_down_action()
        for shape in self.find_all():
            self.delete(shape)

    def get_start_coords(self):
        if len(self.coordinates) > 0:
            return self.coordinates[0]

    def get_coords_increment(self):
        if len(self.coordinates) > 1:
            return map(operator.sub, self.coordinates[-1], self.coordinates[-2])

    def menu_busy_action(self):
        self.menu_clicked = True
