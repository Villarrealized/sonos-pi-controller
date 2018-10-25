import pygame
import pygameui as ui

import color
from main_theme import MainTheme

class MainScene(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)
        # Set the theme
        self.theme = MainTheme()
        ui.theme.use_theme(self.theme)
