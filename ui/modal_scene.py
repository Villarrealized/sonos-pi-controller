from pygame import Rect

from ui.scene import Scene
from ui.image import Image
from ui.button import Button
from ui.label import Label

import ui.colors as colors


class ModalScene(Scene):
    def __init__(self, title):
        Scene.__init__(self)

        self.background_color = colors.MODAL

         # Title label   
        self.title_label = Label(Rect(50,20,220,40),title,40,colors.WHITE)
        self.add_child(self.title_label)

        ##### Close Button #####
        icon_close_image = Image('icon_close',filename='icon_close.png')
        self.close_button = Button(Rect(20,20,30,30),image=icon_close_image)        
        self.close_button.on_tapped.connect(self.close)
        self.add_child(self.close_button)

        self.layout()

    def close(self, button):
        self.remove()