import pygame
import pygameui as ui

class MainScene(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)
        
        self.button = ui.Button(ui.Rect(100,100, 50, 50), 'Test')
        self.add_child(self.button)



