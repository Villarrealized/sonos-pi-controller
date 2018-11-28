from pygame import Rect

from sonos import Sonos

from controller.ui.list_view import ListView
from controller.ui.navigation_scene import NavigationScene
from controller.ui.window import Window

import colors


class SelectFavorite(NavigationScene):
    def __init__(self, sonos, favorites=Sonos.favorites()):
        NavigationScene.__init__(self, "Favorites")


        self.sonos = sonos
        self.background_color = colors.NAVY        

        self.favorites = favorites
        self.favorite_titles = []
        for favorite in self.favorites:
            self.favorite_titles.append(favorite.title)       

        # Add list of favorites
        self.favorite_list_view = ListView(Rect(0,80,Window.frame.width, Window.frame.height - 80),self.favorite_titles)
        self.favorite_list_view.on_selected.connect(self.favorite_selected)
        self.add_child(self.favorite_list_view)

        
    def favorite_selected(self, list_view, title, index):
         print(title)         