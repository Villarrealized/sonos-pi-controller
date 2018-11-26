from pygame import Rect

from sonos import Sonos

from controller.ui.list_view import ListView
from controller.ui.navigation_scene import NavigationScene
from controller.ui.image import Image
from controller.ui.button import Button
from controller.ui.label import Label
from controller.ui.window import Window

import colors


class SelectArtist(NavigationScene):
    def __init__(self, sonos):
        NavigationScene.__init__(self, "Artists")

        self.list_buttons = []
        self.list_index = 0
        self.per_page = 7

        self.artists = [
            "116", 
            "3 Doors Down", 
            "A.R. Rahman", 
            "Aaron Espe", 
            "Acappella", 
            "admin", 
            "Akir", 
            "Albert Mohler", 
            "Alert312", 
            "Alex Faith", 
            "Alex Faith & Dre Murray", 
            "Allen Underwood, Michael Outlaw, Joe Zack : Software Developers", 
            "Aloe Blacc", 
            "Andy Mineo", 
            "Apologia Radio, Jeff Durbin", 
            "Armin Van Buuren", 
            "Art Azurdia", 
            "Atmosphere", 
            "Barbara LaPointe", 
            "Basshunter", 
            "Beatles", 
            "Beautiful Eulogy", 
            "Beautiful Eulogy, Theory Hazit & Lee Green", 
            "Beleaf",
            "Ben Howard",
            "Benjah & Dillavou"
        ]

        self.sonos = sonos
        self.background_color = colors.NAVY

        self.artist_list_view = ListView(Rect(0,80,Window.frame.width, Window.frame.height - 80),self.artists)
        self.artist_list_view.on_selected.connect(self.artist_selected)
        self.add_child(self.artist_list_view)

        
    def artist_selected(self, list_view, artist, index):
         print(artist)
         print(index)