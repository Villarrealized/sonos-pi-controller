import os

from pygame import Rect

from sonos import Sonos

from controller.ui.scene import Scene
from controller.ui.image import Image
from controller.ui.button import Button
from controller.ui.label import Label

import colors


class SelectRoom(Scene):
    def __init__(self, sonos):
        Scene.__init__(self)
        
        self.background_color = colors.MODAL
        self.generate_room_list()

        self.layout()


    def change_room(self, button):        
        self.parent.change_room(button.label.text)
        self.remove()

    def generate_room_list(self):
        y = 80
        for room in Sonos.get_zone_names():
            room_button = Button(Rect(80,y,160,40), 36, text=room)
            room_button.on_tapped.connect(self.change_room)
            self.add_child(room_button)
            y += 60
          