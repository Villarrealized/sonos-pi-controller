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
        self.room_label = Label(Rect(20,20,280,40),"Rooms",40,colors.WHITE)
        self.add_child(self.room_label)

        ##### Close Button #####
        icon_close_image = Image('icon_close',filename='icon_close.png')
        self.close_button = Button(Rect(20,20,30,30),image=icon_close_image)        
        self.close_button.on_tapped.connect(self.close)
        self.add_child(self.close_button)

        self.layout()


    def change_room(self, button):        
        # Get the first room, because it is the coordinator
        self.parent.select_room(button.label.text.split(',')[0])
        self.remove()

    def close(self, button):
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
          