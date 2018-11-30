from pygame import Rect

from sonos import Sonos

from ui.modal_scene import ModalScene
from ui.image import Image
from ui.button import Button
from ui.label import Label

import ui.colors as colors


class GroupRooms(ModalScene):
    def __init__(self, sonos):
        ModalScene.__init__(self, sonos.current_zone)
             
        self.sonos = sonos

        in_party_mode = Sonos.in_party_mode()        

        ##### Party Mode On Button #####        
        icon_party_on_image = Image('icon_party_on',filename='icon_party_on.png')
        self.party_on_button = Button(Rect(270,20,30,30),image=icon_party_on_image)        
        self.party_on_button.hidden = in_party_mode
        self.party_on_button.on_tapped.connect(self.group_all)
        self.add_child(self.party_on_button)

        ##### Party Mode Off Button #####
        icon_party_off_image = Image('icon_party_off',filename='icon_party_off.png')        
        self.party_off_button = Button(Rect(270,20,30,30),image=icon_party_off_image)        
        self.party_off_button.on_tapped.connect(self.group_none)
        self.party_off_button.hidden = not in_party_mode
        self.add_child(self.party_off_button)

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
    
    def group_all(self, button):        
        self.unchanged = False
        self.toggle_party_mode_buttons()
        for button in self.room_buttons:
            button.checked = True     
    
    def group_none(self, button):
        self.unchanged = False
        self.toggle_party_mode_buttons()
        for button in self.room_buttons:
            button.checked = False

    def toggle_party_mode_buttons(self):
        self.party_on_button.hidden = not self.party_on_button.hidden
        self.party_off_button.hidden = not self.party_off_button.hidden


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
                