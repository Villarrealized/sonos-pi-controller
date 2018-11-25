from pygame import Rect

from sonos import Sonos

from controller.ui.list_view import ListView
from controller.ui.navigation_scene import NavigationScene
from controller.ui.image import Image
from controller.ui.button import Button
from controller.ui.label import Label

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

        ##### Previous Button #####
        previous_button_image = Image('previous_button',filename='previous_button.png')
        self.previous_button = Button(Rect(130,420,40,40),image=previous_button_image)        
        self.previous_button.on_tapped.connect(self.previous)
        self.previous_button.hidden = True
        self.add_child(self.previous_button)

        ##### Next Button #####
        next_button_image = Image('next_button',filename='next_button.png')
        self.next_button = Button(Rect(190,420,40,40),image=next_button_image)        
        self.next_button.on_tapped.connect(self.next)
        self.next_button.hidden = True
        self.add_child(self.next_button)

        self.layout()

        self.create_artist_list()

        self.next(None)



    def create_artist_list(self):
        # Clean up any old buttons before addings new ones
        for button in self.list_buttons:
            self.remove()

        self.update_list_navigation()

        y = 80
        for index, artist in enumerate(self.artists):
            if index >= self.list_index and index < self.per_page:
                artist_button = Button(Rect(40,y,240,30), 30, Label.LEFT, text=artist)
                artist_button.on_tapped.connect(self.select_artist)
                self.add_child(artist_button)
                self.list_buttons.append(artist_button)
                y += 50


    def select_artist(self, button):
        print(self.button.text)

    def update_list_navigation(self):
        num_artists = len(self.artists)
        if num_artists == 0: return   

        if (self.list_index + self.per_page) < num_artists:
            self.next_button.hidden = False
        else:
            self.next_button.hidden = True
        
        if (self.list_index - self.per_page) >= 0:
            self.previous_button.hidden = False
        else:
            self.previous_button.hidden = True


    def next(self, button):
        self.list_index += self.per_page
        self.create_artist_list()

    def previous(self, button):
        self.list_index -= self.per_page
        self.create_artist_list

