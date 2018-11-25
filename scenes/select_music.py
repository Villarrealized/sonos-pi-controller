from pygame import Rect

from sonos import Sonos

from controller.ui.list_view import ListView
from controller.ui.modal_scene import ModalScene
from scenes.select_artist import SelectArtist
from controller.ui.image import Image
from controller.ui.button import Button
from controller.ui.label import Label

import colors


class SelectMusic(ModalScene):

    CATEGORIES = ['Artists', 'Albums', 'Genres', 'Favorites', 'Playlists']

    def __init__(self, sonos):
        ModalScene.__init__(self, "Music Library")

        self.sonos = sonos
        self.background_color = colors.NAVY
        self.layout()

        self.create_library_list()

        ### Testing ###
        self.select_library_option('Artists')



    def create_library_list(self):
        y = 80
        for category in SelectMusic.CATEGORIES:
            library_option_button = Button(Rect(40,y,240,40), 34, Label.LEFT, text=category)
            library_option_button.on_tapped.connect(self.select_library_option)
            self.add_child(library_option_button)            
            y += 80

    # def select_library_option(self, button):
    #     option = button.label.text
    #     print(option)


    def select_library_option(self, text):
        option = text
        print(option)

        if option == 'Artists':
            artistScene = SelectArtist(self.sonos)
            self.add_child(artistScene)
