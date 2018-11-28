import pygame

from view import View
from label import Label
from callback_signal import Signal
import ui.colors as colors

class Button(View):
    """A button that can have an image or a label or both.
    Can connect a callback
    """
    def __init__(self, frame, font_size=30, text_align=Label.CENTER, **kwargs):
        View.__init__(self,frame)        

        self._original_image = None
        self._disabled_image = None
        self._checked_image = None
        self.image = None
        self.label = None
        self.font_size = font_size

        self._checked = False
        
        self.on_tapped = Signal()

        for key, value in kwargs.items():
            if key == 'image':                
                self._original_image = value
                self.image = value
            if key == 'disabled_image':
                self._disabled_image = value
            if key == 'checked_image':
                self._checked_image = value
            if key == 'text':                      
                self.label = Label(self.frame, value, self.font_size, colors.WHITE, text_align)   


    @property
    def checked(self):
        return self._checked

    @checked.setter                                    
    def checked(self, checked):
        self._checked = checked
        if not self._checked:
            self.image = self._original_image
        elif self._checked_image is not None:
            self.image = self._checked_image
                
             
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
        if self.image is not None and self.label is not None:
            self.surface = pygame.Surface(self.frame.size, pygame.SRCALPHA, 32).convert_alpha()
            self.surface.blit(self.image.surface, (0,0))            
            self.surface.blit(self.label.surface,(self.image.surface.get_width() + 10,0))
        elif self.image is not None:
            self.surface = self.image.surface
        elif self.label is not None:
            self.surface = self.label.surface

    def mouse_up(self, button, point):
        self.on_tapped(self)
