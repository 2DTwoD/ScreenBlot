import pynput


class MouseCoordinate:
    def __init__(self, root_canvas):
        self.root_canvas = root_canvas
        mouse_listener = pynput.mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        mouse_listener.start()

    def on_move(self, x, y):
        self.root_canvas.event_generate('<<Screen_mouse_move>>', x=x, y=y)

    def on_click(self, x, y, button, pressed):
        if button == pynput.mouse.Button.left:
            if pressed:
                self.root_canvas.event_generate('<<Screen_lmouse_down>>', x=x, y=y)
            else:
                self.root_canvas.event_generate('<<Screen_lmouse_up>>', x=x, y=y)
        elif button == pynput.mouse.Button.right:
            self.root_canvas.event_generate('<<Screen_rmouse_down>>', x=x, y=y)

