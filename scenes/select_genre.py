from pygame import Rect

from sonos import Sonos

from ui.list_view import ListView
from ui.navigation_scene import NavigationScene
from ui.window import Window

from scenes.select_artist import SelectArtist

import ui.colors as colors


class SelectGenre(NavigationScene):
    def __init__(self, sonos, genres=Sonos.genres()):
        NavigationScene.__init__(self, "Genres")

        self.sonos = sonos
        self.background_color = colors.NAVY        

        self.genres = genres
        self.genre_titles = []
        for genre in self.genres:
            self.genre_titles.append(genre.title)       

        # Add list of genres
        self.genre_list_view = ListView(Rect(0,80,Window.frame.width, Window.frame.height - 80),self.genre_titles)
        self.genre_list_view.on_selected.connect(self.genre_selected)
        self.add_child(self.genre_list_view)

        
    def genre_selected(self, list_view, title, index):
         # Browse the artists for this genre
        scene = SelectArtist(self.sonos,title,Sonos.browse(self.genres[index]))
        self.add_child(scene)
