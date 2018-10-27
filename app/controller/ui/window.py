
class Window:
    """ Everything is drawn to the window. Only need 1 instance. Should never change."""
    def __init__(self, frame):
        # A Scene is a View that fills the entire screen and can be changed
        self.scene = None
        # the bounds of the window
        self.frame = frame
        # pygame Surface used to draw on
        self.surface = None

        