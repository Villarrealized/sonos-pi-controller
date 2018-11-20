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

        # Rooms label   
        self.room_label = Label(Rect(50,20,220,40),"Rooms",40,colors.WHITE)
        self.add_child(self.room_label)

        ##### Close Button #####
        icon_close_image = Image('icon_close',filename='icon_close.png')
        self.close_button = Button(Rect(20,20,30,30),image=icon_close_image)        
        self.close_button.on_tapped.connect(self.close)
        self.add_child(self.close_button)

        self.layout()


    def change_room(self, button):        
        self.parent.change_room(button.label.text)
        self.remove()

    def close(self, button):
        self.remove()

    def generate_room_list(self):
        y = 80
        for room in Sonos.get_zone_names():
            room_button = Button(Rect(80,y,160,40), 30, text=room)
            room_button.on_tapped.connect(self.change_room)
            self.add_child(room_button)
            y += 60
          