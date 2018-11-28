from pygame import Rect

from sonos import Sonos

from ui.list_view import ListView
from ui.navigation_scene import NavigationScene
from ui.window import Window

from scenes.select_album import SelectAlbum

import ui.colors as colors


class SelectArtist(NavigationScene):
    def __init__(self, sonos, title="Artists", artists=Sonos.artists()):
        NavigationScene.__init__(self, title)
        
        self.sonos = sonos
        self.background_color = colors.NAVY        

        self.artists = artists
        self.artist_titles = []
        for artist in self.artists:
            self.artist_titles.append(artist.title)       

        # Add list of artists
        self.artist_list_view = ListView(Rect(0,80,Window.frame.width, Window.frame.height - 80),self.artist_titles)
        self.artist_list_view.on_selected.connect(self.artist_selected)
        self.add_child(self.artist_list_view)

        
    def artist_selected(self, list_view, title, index):
        # Browse the albums for this artist
        scene = SelectAlbum(self.sonos,title,Sonos.browse(self.artists[index]))
        self.add_child(scene)