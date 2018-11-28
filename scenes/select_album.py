from pygame import Rect

from sonos import Sonos

from controller.ui.list_view import ListView
from controller.ui.navigation_scene import NavigationScene
from controller.ui.window import Window

import colors


class SelectAlbum(NavigationScene):
    def __init__(self, sonos, title="Albums", albums=Sonos.albums()):
        NavigationScene.__init__(self, title)


        self.sonos = sonos
        self.background_color = colors.NAVY        

        self.albums = albums
        self.album_titles = []
        for album in self.albums:
            self.album_titles.append(album.title)       

        # Add list of albums
        self.album_list_view = ListView(Rect(0,80,Window.frame.width, Window.frame.height - 80),self.album_titles)
        self.album_list_view.on_selected.connect(self.album_selected)
        self.add_child(self.album_list_view)

        
    def album_selected(self, list_view, album, index):
         print(album)
         print(index)