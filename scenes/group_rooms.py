from pygame import Rect

from sonos import Sonos

from controller.ui.modal_scene import ModalScene
from controller.ui.image import Image
from controller.ui.button import Button
from controller.ui.label import Label

import colors


class GroupRooms(ModalScene):
    def __init__(self, sonos):
        ModalScene.__init__(self, sonos.current_zone)
             
        self.sonos = sonos   

        ##### Done Button #####        
        self.done_button = Button(Rect(20,430,280,40),40 ,text='Done')        
        self.done_button.on_tapped.connect(self.done)
        self.add_child(self.done_button)                

        self.room_buttons = []

        self.unchanged = True

        self.layout()
        self.generate_rooms()

    def done(self, button):
        if not self.unchanged:
            rooms = []
            for button in self.room_buttons:            
                rooms.append({
                    "name": button.label.text,
                    "join": button.checked
                })

            self.parent.group_rooms(rooms)
        self.remove()            

    def select_room(self, button):
        self.unchanged = False
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