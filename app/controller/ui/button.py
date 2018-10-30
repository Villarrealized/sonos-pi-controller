from view import View

class Button(View):
    """A button that can have an image.
    Can connect a callback
    TODO: Add support for a text label
    
    """
    def __init__(self, frame, **kwargs):
         View.__init__(self,frame)

         self.image = None

         for key, value in kwargs.items():
             if key == 'image':
                 self.image = value
    
    def draw (self):
        self.surface = self.image.surface
