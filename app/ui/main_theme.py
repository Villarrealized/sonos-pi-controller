import pygame
import pygameui as ui
import color

class MainTheme(ui.theme.Theme):
    def __init__(self):
        ui.theme.Theme.__init__(self)
        
        self.set(class_name='View', state='normal', key='background_color',value=color.NAVY)
        self.set(class_name='View',
                    state='normal',
                    key='shadowed',
                    value=False)
                    