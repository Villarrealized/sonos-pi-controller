import pkg_resources
import os
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

        self.play_button = ui.ImageButton(ui.Rect(294,181,60,60),pygame.image.load('/usr/src/app/resources/images/play_track.png'))
        self.add_child(self.play_button)
