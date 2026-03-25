import tkinter as tk


class AutosizeEntry(tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent, *args, **kwargs)
        self.insert(0, 'Текст')
        self.config(width=len(self.get()), validate='key', validatecommand=(self.register(self.resize_action), "%P"), bd=0)
        self.bind('<FocusIn>', lambda e: self.select_range(0, tk.END))

    def resize_action(self, newval):
        self.config(width=len(newval) + 1)
        return True
