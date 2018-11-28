import pygame
from pygame.font import Font

from view import View
import ui.colors as colors

class Label(View):

    CENTER=0
    LEFT=1

    def __init__(self, frame, text, font_size=18, color=colors.WHITE, halign=0, valign=0):
        View.__init__(self, frame)

        self.font = Font(None, font_size)
        self.halign = halign
        self.valign = valign
        self._text = text
        self._enabled = False
        self.color = color        

        self.layout()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self.render()

    def layout(self):
        self.render()

    def render(self):
        self._render(self._text)

    def _render(self, text):        
        if text is None or len(text) == 0:
            self.hidden = True
        else:
            self.hidden = False

        self._render_line(self._text)        

    def _render_line(self, line_text):
        line_text = line_text.strip()     
        # Create a transparent background
        self.surface = pygame.Surface(self.frame.size, pygame.SRCALPHA, 32).convert_alpha()        
        # Add the text
        self.text_surface = self.font.render(line_text, True, self.color)

        text_position = (0,0)
        text_width = self.text_surface.get_size()[0]
        text_height = self.text_surface.get_size()[1]
        if self.halign == self.CENTER:            
            text_position = ((self.frame.width - text_width) // 2, 0)
        elif self.halign == self.LEFT and self.valign == self.CENTER:
            text_position = (0, (self.frame.height - text_height) //2)

        

        # Make sure the beginning of the text can be seen 
        # if the width is too big for the screen
        if text_width > self.frame.width:            
            text_position = (0,0)

        self.surface.blit(self.text_surface, text_position)
        


    def __repr__(self):
        if self._text is None:
            return ''
        return self._text