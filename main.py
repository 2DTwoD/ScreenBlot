import tkinter as tk

from mouse_coordinate import MouseCoordinate
from root_canvas import RootCanvas


transparent_color = '#ABCDEF'


def main():
    root = tk.Tk()
    root.config(background=transparent_color)
    root.attributes('-transparentcolor', transparent_color)
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)

    root_canvas = RootCanvas(root, transparent_color)
    root_canvas.pack(fill=tk.BOTH, expand=True)

    MouseCoordinate(root_canvas)

    root.mainloop()


if __name__ == '__main__':
    main()
