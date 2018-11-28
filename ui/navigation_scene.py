from pygame import Rect

from ui.scene import Scene
from ui.image import Image
from ui.button import Button
from ui.label import Label

import ui.colors as colors


class NavigationScene(Scene):
    def __init__(self, title):
        Scene.__init__(self)

        self.background_color = colors.MODAL

         # Title label   
        self.title_label = Label(Rect(50,20,220,40),title,40,colors.WHITE)
        self.add_child(self.title_label)

        ##### Back Button #####
        icon_back_image = Image('icon_back',filename='icon_back.png')
        self.back_button = Button(Rect(20,20,30,30),image=icon_back_image)        
        self.back_button.on_tapped.connect(self.back)
        self.add_child(self.back_button)

        self.layout()

    def back(self, button):
        self.remove()