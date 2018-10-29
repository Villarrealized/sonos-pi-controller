from view import View
from window import Window

class Scene(View):
    """A view that takes up the entire window content area."""

    def __init__(self):
        View.__init__(self)
        # A scenes frame is ALWAYS equal to the windows frame
        self.frame = Window.frame
        # Need to layout now that we have adjusted the frame
        self.layout()