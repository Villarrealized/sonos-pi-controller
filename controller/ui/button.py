from view import View
from label import Label
from callback_signal import Signal

class Button(View):
    """A button that can have an image or a label.
    Can connect a callback
    TODO: Add support for a text label
    
    """
    def __init__(self, frame, font_size=30, **kwargs):
        View.__init__(self,frame)        

        self._original_image = None
        self._disabled_image = None
        self.image = None
        self.label = None
        self.font_size = font_size
        
        self.on_tapped = Signal()

        for key, value in kwargs.items():
            if key == 'image':
                self._original_image = value
                self.image = value
            if key == 'disabled_image':
                self._disabled_image = value
            if key == 'text':                
                self.label = Label(self.frame,value,self.font_size)                                       
                
             
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
        if self.image is not None:
            self.surface = self.image.surface
        elif self.label is not None:
            self.surface = self.label.surface

    def mouse_up(self, point):
        self.on_tapped(self)
