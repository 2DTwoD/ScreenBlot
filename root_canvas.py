import operator
import tkinter as tk
from enum import Enum


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

        close.pack(anchor=tk.NE)
        clear.pack(anchor=tk.NE)
        undo.pack(anchor=tk.NE)

        self.type = ShapeType.TEXT

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

    def global_mouse_move_action(self, x, y):
        if self.mouse_down or self.start_click_drawing:
            self.coordinates.append((x, y))
            if self.shape_for_moving is None:
                self.after(0, lambda: self.draw_shape())
            else:
                self.move(self.shape_for_moving, *self.get_coords_increment())

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

    def draw_shape(self):
        if self.shape_id is not None:
            self.delete(self.shape_id)
        match self.type:
            case ShapeType.LINE:
                self.shape_id = self.create_oval(self.coordinates, width=3, outline='white')
                self.shape_id = self.create_line(self.coordinates, width=3, fill='white')
            case ShapeType.RECTANGLE:
                self.shape_id = self.create_rectangle(self.coordinates, width=3, outline='white')
                self.coordinates.pop(-1)
            case ShapeType.OVAL:
                self.coordinates.pop(-1)
            case ShapeType.POLYGON:
                self.shape_id = self.create_polygon(self.coordinates, width=3, outline='white', fill='red')
                self.coordinates.pop(-1)
            case ShapeType.TEXT:
                self.shape_id = self.create_text(self.get_start_coords(), fill="red", text="Test")
                self.coordinates.pop(-1)

    def end_drawing(self):
        self.coordinates.clear()
        self.shape_for_moving = None
        if self.shape_id is None:
            return
        tmp_shape_id = self.shape_id
        self.tag_bind(self.shape_id, '<Button-1>', lambda e: self.shape_click_action(tmp_shape_id))
        self.tag_bind(self.shape_id, '<Button-3>', lambda e: self.delete(tmp_shape_id))
        self.shape_id = None

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
