import pygame
import pygameui as ui
import sys
sys.path.append("..")
import color

class MainScene(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)
        self.background_color = color.NAVY
        



