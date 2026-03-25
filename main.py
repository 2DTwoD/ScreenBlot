import faulthandler
import tkinter as tk

from mouse_coordinate import MouseCoordinate
from root_canvas import RootCanvas


transparent_color = '#ABCDEF'


def main():
    faulthandler.enable()
    root = tk.Tk()

    root.geometry('500x500')
    root.attributes('-transparentcolor', transparent_color)
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.config(background=transparent_color)

    root_canvas = RootCanvas(root)
    root_canvas.place(x=0, y=0)

    MouseCoordinate(root_canvas)

    root_canvas.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == '__main__':
    main()
