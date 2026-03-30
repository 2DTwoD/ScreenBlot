import threading
import time
import tkinter as tk
from enum import Enum

from color_panel import ColorPanel


class ShapeType(Enum):
    NONE = 0
    PENCIL = 1
    RECTANGLE = 2
    OVAL = 3
    POLYGON = 4
    TEXT = 5


class InstrumentPanel(tk.Frame):
    def __init__(self, parent, root, transparent_color, clear_action, undo_action, menu_busy_action):
        tk.Frame.__init__(self, parent, background=transparent_color)

        self.type = ShapeType.NONE

        close = tk.Button(self, text='X', command=root.destroy, width=3, font='Courier 10 bold', background='red')
        minimize = tk.Button(self, text='-', command=root.iconify, width=3, font='Courier 10 bold', background='orange')
        clear = tk.Button(self, text='C', command=clear_action, width=3, font='Courier 10 bold', background='yellow')
        undo = tk.Button(self, text='<-', command=undo_action, width=3, font='Courier 10 bold', background='yellow')

        self.border_color_panel = ColorPanel(self, menu_busy_action, default_color='black')
        self.fill_color_panel = ColorPanel(self, menu_busy_action, default_color='white')

        self.instrument_buttons = []
        self.instrument_buttons.append(tk.Button(self, text='.', command=lambda: self.setType(ShapeType.NONE), width=3,
                                                 font='Courier 10 bold'))
        self.instrument_buttons.append(
            tk.Button(self, text='~', command=lambda: self.setType(ShapeType.PENCIL), width=3,
                      font='Courier 10 bold'))
        self.instrument_buttons.append(
            tk.Button(self, text='□', command=lambda: self.setType(ShapeType.RECTANGLE), width=3,
                      font='Courier 10 bold'))
        self.instrument_buttons.append(tk.Button(self, text='O', command=lambda: self.setType(ShapeType.OVAL), width=3,
                                                 font='Courier 10 bold'))
        self.instrument_buttons.append(
            tk.Button(self, text='L', command=lambda: self.setType(ShapeType.POLYGON), width=3,
                      font='Courier 10 bold'))
        self.instrument_buttons.append(tk.Button(self, text='T', command=lambda: self.setType(ShapeType.TEXT), width=3,
                                                 font='Courier 10 bold'))
        self.border_color_button = tk.Button(self, text='⬠', background='lightgray',
                                             command=lambda: self.open_color_panel(self.border_color_panel,
                                                                                   self.fill_color_panel),
                                             width=3, font='Courier 10 bold')
        self.fill_color_button = tk.Button(self, text='⬟', background='lightgray',
                                           command=lambda: self.open_color_panel(self.fill_color_panel,
                                                                                 self.border_color_panel),
                                           width=3, font='Courier 10 bold')

        close.pack(anchor=tk.NE)
        minimize.pack(anchor=tk.NE)
        clear.pack(anchor=tk.NE)
        undo.pack(anchor=tk.NE)

        for button in self.instrument_buttons:
            button.pack(anchor=tk.NE)

        self.border_color_button.pack(anchor=tk.NE)
        self.fill_color_button.pack(anchor=tk.NE)

        for child in self.winfo_children():
            child.bind('<Button-1>', lambda e: menu_busy_action())

        threading.Thread(target=self.update, daemon=True).start()

    def open_color_panel(self, show_panel, hide_panel):
        if show_panel.winfo_viewable():
            show_panel.pack_forget()
        else:
            show_panel.pack()
        hide_panel.pack_forget()

    def close_color_panels(self):
        self.border_color_panel.pack_forget()
        self.fill_color_panel.pack_forget()

    def border_color_panel_opened(self):
        return self.border_color_panel.winfo_viewable()

    def fill_color_panel_opened(self):
        return self.fill_color_panel.winfo_viewable()

    def setType(self, new_type):
        self.type = new_type

    def update(self):
        while True:
            for index, button in enumerate(self.instrument_buttons):
                if index == self.type.value:
                    button.config(background='lightgreen')
                else:
                    button.config(background='lightgray')

            self.update_color_button(self.border_color_button, self.border_color_panel)
            self.update_color_button(self.fill_color_button, self.fill_color_panel)

            time.sleep(0.2)

    @staticmethod
    def update_color_button(button, panel):
        if panel.color == '':
            bg = 'gray' if panel.winfo_viewable() else 'black'
            button.config(background=bg, foreground='white')
        else:
            bg = 'gray' if panel.winfo_viewable() else 'lightgray'
            button.config(background=bg, foreground=panel.color)

    def get_border_color(self):
        return self.border_color_panel.color

    def get_fill_color(self):
        return self.fill_color_panel.color

    def return_border_color(self):
        self.border_color_panel.return_prev_color()

    def return_fill_color(self):
        self.fill_color_panel.return_prev_color()
