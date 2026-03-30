import tkinter as tk


class ColorPanel(tk.Frame):
    def __init__(self, parent, menu_busy_action, default_color='black'):
        tk.Frame.__init__(self, parent)
        self.color = default_color
        self.prev_color = default_color
        self._new_color_button('black')
        self._new_color_button('white')
        self._new_color_button('red')
        self._new_color_button('hot pink')
        self._new_color_button('orange')
        self._new_color_button('brown')
        self._new_color_button('yellow')
        self._new_color_button('burlywood4')
        self._new_color_button('green')
        self._new_color_button('OliveDrab4')
        self._new_color_button('cyan')
        self._new_color_button('cyan4')
        self._new_color_button('blue')
        self._new_color_button('blue4')
        self._new_color_button('purple')
        self._new_color_button('medium purple')

        without_color = tk.Button(self, command=lambda: self._set_color(''), width=3, background='black',
                                  foreground='white', text='x')
        without_color.pack()

        for child in self.winfo_children():
            child.bind('<Button-1>', lambda e: menu_busy_action())

    def _new_color_button(self, color: str):
        color_button = tk.Button(self, command=lambda: self._set_color(color), width=3, background=color)
        color_button.pack()

    def _set_color(self, color: str, ):
        if self.color != color:
            self.prev_color = self.color
            self.color = color
        self.pack_forget()

    def is_no_color(self):
        return self.color == ''

    def return_prev_color(self):
        self.color = self.prev_color
