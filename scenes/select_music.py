from pygame import Rect

from sonos import Sonos

from controller.ui.scene import Scene
from controller.ui.image import Image
from controller.ui.button import Button
from controller.ui.label import Label

import colors


class SelectMusic(Scene):

    CATEGORIES = ['Artists', 'Albums', 'Genres', 'Favorites', 'Playlists']

    def __init__(self, sonos):
        Scene.__init__(self)

        self.sonos = sonos
        self.background_color = colors.NAVY

         # Title
        self.title_label = Label(Rect(50,20,220,40),"Music Library",40,colors.WHITE)
        self.add_child(self.title_label)

        ##### Close Button #####
        icon_close_image = Image('icon_close',filename='icon_close.png')
        self.close_button = Button(Rect(20,20,30,30),image=icon_close_image)        
        self.close_button.on_tapped.connect(self.close)
        self.add_child(self.close_button)

        self.layout()

        self.create_library_list()

        

    def close(self, button):
        self.remove()

    def create_library_list(self):
        y = 80
        for category in SelectMusic.CATEGORIES :
            library_option_button = Button(Rect(40,y,240,40), 34, Label.LEFT, text=category)
            library_option_button.on_tapped.connect(self.select_library_option)
            self.add_child(library_option_button)            
            y += 80

    def select_library_option(self, button):
        print(button.label.text)