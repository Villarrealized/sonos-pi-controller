from pygame import Rect

from sonos import Sonos

from controller.ui.modal_scene import ModalScene
from controller.ui.image import Image
from controller.ui.button import Button
from controller.ui.label import Label

import colors


class SelectRoom(ModalScene):
    def __init__(self, sonos):
        ModalScene.__init__(self, "Rooms")

        self.generate_room_list()
        self.layout()


    def change_room(self, button):        
        # Get the first room, because it is the coordinator
        self.parent.select_room(button.label.text.split(',')[0])
        self.remove()

    def generate_room_list(self):
        ''' Generates a list of rooms/zones

        If a room is a zone coordinator and has members in its group,
        it will be displayed first with all its members appended to it
        with commas'''
        y = 80
        for zone in Sonos.get_zone_groups():
            if zone["is_coordinator"]:
                button_text = zone["name"]
                for member in zone["members"]:
                    button_text += ", {}".format(member)
                room_button = Button(Rect(20,y,280,40), 30, text=button_text)
                room_button.on_tapped.connect(self.change_room)
                self.add_child(room_button)
                y += 60
          