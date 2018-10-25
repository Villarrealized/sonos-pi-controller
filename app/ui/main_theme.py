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
        self.set(class_name='View',
                    state='normal',
                    key='border_color',
                    value=None)

        self.set(class_name='ImageView',
                    state='normal',
                    key='padding',
                    value=(0, 0))
        self.set(class_name='ImageView',
                    state='normal',
                    key='background_color',
                    value=None)   

        self.set(class_name='ImageButton',
                    state='normal',
                    key='padding',
                    value=(6, 6))
        self.set(class_name='ImageButton',
                    state='normal',
                    key='border_color',
                    value=None)
        self.set(class_name='ImageButton',
                    state='normal',
                    key='border_widths',
                    value=None)
                    