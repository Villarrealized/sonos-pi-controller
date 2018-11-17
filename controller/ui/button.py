from view import View
from callback_signal import Signal

class Button(View):
    """A button that can have an image.
    Can connect a callback
    TODO: Add support for a text label
    
    """
    def __init__(self, frame, **kwargs):
        View.__init__(self,frame)        

        self._original_image = None
        self._disabled_image = None
        self.image = None
        
        self.on_tapped = Signal()

        for key, value in kwargs.items():
            if key == 'image':
                self._original_image = value
                self.image = value
            if key == 'disabled_image':
                self._disabled_image = value
             
    @property
    def enabled(self):
        return self._enabled
    @enabled.setter
    def enabled(self, enabled):
        self._enabled = enabled
        if self._enabled:
            self.image = self._original_image
        elif self._disabled_image is not None:
            self.image = self._disabled_image

    def draw (self):
        self.surface = self.image.surface

    def mouse_up(self, point):
        self.on_tapped(self)
