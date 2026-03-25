import tkinter as tk


class AutosizeEntry(tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        tk.Entry.__init__(self, parent, *args, **kwargs)
        self.config(width=len(self.get()), validate='key', validatecommand=(self.register(self.resize_action), "%P"), bd=0)

    def resize_action(self, newval):
        self.config(width=len(newval) + 1)
        return True
