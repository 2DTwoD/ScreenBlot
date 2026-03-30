import operator
import tkinter as tk

from autosize_entry import AutosizeEntry
from instrument_panel import InstrumentPanel, ShapeType


def type_none_check(func):
    def wrapper(self, x=0, y=0):
        if self.i_panel.type == ShapeType.NONE and self.shape_for_moving is None or self.root.wm_state() == 'iconic':
            return lambda self, x, y: None
        return func(self, x, y)
    return wrapper


class RootCanvas(tk.Canvas):
    def __init__(self, root, transparent_color):
        tk.Canvas.__init__(self, root, bg=transparent_color, bd=0, highlightthickness=0)

        self.root = root

        self.i_panel = InstrumentPanel(self, root, transparent_color, self.clear_action, self.undo_action,
                                       self.menu_busy_action)
        self.i_panel.pack(anchor=tk.NE)

        self.bind("<<Screen_lmouse_down>>", lambda e: self.after(1, self.lmouse_down_action, e.x, e.y))
        self.bind("<<Screen_lmouse_up>>", lambda e: self.after(1, self.lmouse_up_action, e.x, e.y))
        self.bind("<<Screen_mouse_move>>", lambda e: self.after(1, self.mouse_move_action, e.x, e.y))
        self.bind("<<Screen_rmouse_down>>", lambda e: self.after(1, self.rmouse_down_action, e.x, e.y))

        self.entry = None
        self.shape_id = None

        self.mouse_down = False
        self.start_click_drawing = False
        self.menu_clicked = False

        self.coordinates = []

        self.shape_for_moving = None
        self.move_shift_x = 0
        self.move_shift_y = 0

    @type_none_check
    def lmouse_down_action(self, x=0, y=0):
        if self.menu_clicked:
            self.menu_clicked = False
            return
        self.i_panel.close_color_panels()
        self.mouse_down = True
        self.coordinates.append((x, y))
        if self.shape_for_moving is None:
            self.start_click_drawing = self.i_panel.type == ShapeType.POLYGON
            if self.i_panel.type == ShapeType.TEXT:
                self.draw_shape()

    @type_none_check
    def mouse_move_action(self, x=0, y=0):
        if self.shape_for_moving is not None:
            self.coordinates.append((x, y))
            self.move(self.shape_for_moving, *self.get_coords_increment())
        elif self.i_panel.type == ShapeType.TEXT:
            return
        elif self.mouse_down or self.start_click_drawing:
            self.draw_shape(x, y)

    @type_none_check
    def lmouse_up_action(self, x=0, y=0):
        self.mouse_down = False
        if self.i_panel.type == ShapeType.POLYGON:
            if self.shape_for_moving is not None:
                self.coordinates.clear()
                self.shape_for_moving = None
            return
        self.end_drawing()

    @type_none_check
    def rmouse_down_action(self, x=0, y=0):
        if self.start_click_drawing:
            self.end_drawing()
            self.start_click_drawing = False

    def draw_shape(self, x=0, y=0):
        if self.shape_id is not None:
            self.delete(self.shape_id)
        match self.i_panel.type:
            case ShapeType.PENCIL:
                self.coordinates.append((x, y))
                if self.i_panel.get_fill_color() == '':
                    self.check_border_color()
                    self.shape_id = self.create_line(self.coordinates, width=3,
                                                     fill=self.i_panel.get_border_color())
                else:
                    self.shape_id = self.create_polygon(*self.coordinates, x, y, width=3,
                                                        outline=self.i_panel.get_border_color(),
                                                        fill=self.i_panel.get_fill_color())
            case ShapeType.RECTANGLE:
                self.check_colors()
                self.shape_id = self.create_rectangle(*self.coordinates, x, y, width=3,
                                                      outline=self.i_panel.get_border_color(),
                                                      fill=self.i_panel.get_fill_color())
            case ShapeType.OVAL:
                self.check_colors()
                self.shape_id = self.create_oval(*self.coordinates, x, y, width=3,
                                                 outline=self.i_panel.get_border_color(),
                                                 fill=self.i_panel.get_fill_color())
            case ShapeType.POLYGON:
                self.check_border_color()
                self.shape_id = self.create_polygon(*self.coordinates, x, y, width=3,
                                                    outline=self.i_panel.get_border_color(),
                                                    fill=self.i_panel.get_fill_color())
            case ShapeType.TEXT:
                self.check_border_color()
                self.check_fill_color()
                self.entry = AutosizeEntry(self, font='Courier 20 bold',
                                           fg=self.i_panel.get_border_color(),
                                           bg=self.i_panel.get_fill_color())
                self.shape_id = self.create_window(self.get_start_coords(), window=self.entry)

    def check_colors(self):
        if self.i_panel.get_fill_color() == '' and self.i_panel.get_border_color() == '':
            self.i_panel.return_border_color()

    def check_border_color(self):
        if self.i_panel.get_border_color() == '':
            self.i_panel.return_border_color()

    def check_fill_color(self):
        if self.i_panel.get_fill_color() == '':
            self.i_panel.return_fill_color()

    def end_drawing(self):
        self.coordinates.clear()
        self.shape_for_moving = None
        if self.shape_id is None:
            return
        tmp_shape_id = self.shape_id
        if self.i_panel.type == ShapeType.TEXT and self.entry is not None:
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
        self.rmouse_down_action()
        self.menu_clicked = self.i_panel.type != ShapeType.NONE
