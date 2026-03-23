import pynput


class MouseCoordinate:
    def __init__(self, root_canvas):
        self.pressed = False
        self.root_canvas = root_canvas
        mouse_listener = pynput.mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        mouse_listener.start()

    def on_move(self, x, y):
        if self.pressed:
            self.root_canvas.new_coordinate(x, y)

    def on_click(self, x, y, button, pressed):
        if button == pynput.mouse.Button.left:
            self.pressed = pressed
            if pressed:
                self.root_canvas.start_drawing(x, y)
            else:
                self.root_canvas.end_drawing()

