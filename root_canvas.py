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
        clear = tk.Button(self, text='C', command=self.clear_action, width=3)
        undo = tk.Button(self, text='<--', command=self.undo_action, width=3)

        self.transparent_color = transparent_color

        close.pack(anchor=tk.NE)
        clear.pack(anchor=tk.NE)
        undo.pack(anchor=tk.NE)

        self.type = ShapeType.LINE

        self.entry = None

        self.mouse_down = False
        self.start_click_drawing = False

        self.coordinates = []

        self.shape_id = None

        self.shape_for_moving = None
        self.move_shift_x = 0
        self.move_shift_y = 0

    def global_lmouse_down_action(self, x, y):
        self.mouse_down = True
        self.start_click_drawing = self.type == ShapeType.POLYGON
        self.coordinates.append((x, y))
        if self.type == ShapeType.TEXT:
            self.after(1, lambda: self.draw_shape() if self.shape_for_moving is None else None)

    def global_mouse_move_action(self, x, y):
        if self.shape_for_moving is not None:
            self.coordinates.append((x, y))
            self.move(self.shape_for_moving, *self.get_coords_increment())
        elif self.mouse_down:
            self.after(0, lambda: self.draw_shape(x, y))

    def global_lmouse_up_action(self, x, y):
        self.mouse_down = False
        if self.type == ShapeType.POLYGON:
            self.shape_for_moving = None
            return
        self.end_drawing()

    def global_rmouse_down_action(self, x, y):
        if self.start_click_drawing:
            self.after(1, self.end_drawing)
            self.coordinates.clear()
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
        if len(self.find_all()) > 0:
            self.delete(self.find_all()[-1])

    def clear_action(self):
        for shape in self.find_all():
            self.delete(shape)

    def get_start_coords(self):
        if len(self.coordinates) > 0:
            return self.coordinates[0]

    def get_coords_increment(self):
        if len(self.coordinates) > 1:
            return map(operator.sub, self.coordinates[-1], self.coordinates[-2])
