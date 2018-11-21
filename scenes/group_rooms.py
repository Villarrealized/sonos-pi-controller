import os

from pygame import Rect

from sonos import Sonos

from controller.ui.scene import Scene
from controller.ui.image import Image
from controller.ui.button import Button
from controller.ui.label import Label

import colors


class GroupRooms(Scene):
    def __init__(self, sonos):
        Scene.__init__(self)

        self.sonos = sonos
        self.background_color = colors.MODAL

        # Rooms label   
        self.room_label = Label(Rect(50,20,200,40),self.sonos.current_zone,40,colors.WHITE)
        self.add_child(self.room_label)

         ##### Close Button #####
        icon_close_image = Image('icon_close',filename='icon_close.png')
        self.close_button = Button(Rect(20,20,30,30),image=icon_close_image)        
        self.close_button.on_tapped.connect(self.close)
        self.add_child(self.close_button)

        ##### Done Button #####        
        self.done_button = Button(Rect(20,430,280,40),40 ,text='Done')        
        self.done_button.on_tapped.connect(self.done)
        self.add_child(self.done_button)                

        self.room_buttons = []

        self.layout()
        self.generate_rooms()

    def close(self, button):
        self.remove()

    def done(self, button):
        for button in self.room_buttons:
            print(button.label.text + ": " + button.checked)            

    def select_room(self, button):
        button.checked = not button.checked

    def generate_rooms(self):
        checkbox_empty_image = Image('checkbox_empty',filename='checkbox_empty.png')
        checkbox_filled_image = Image('checkbox_filled',filename='checkbox_filled.png')
        members = self.sonos.group_members
        y = 80
        for zone in self.sonos.potential_members:
            select_room_button = Button(Rect(60,y,280,30), 34, Label.LEFT,image=checkbox_empty_image, checked_image=checkbox_filled_image, text=zone)
            select_room_button.on_tapped.connect(self.select_room)
            self.add_child(select_room_button)
            self.room_buttons.append(select_room_button)
            y += 60
            
            if zone in members:
                # this zone is already a member
                select_room_button.checked = True