from pygame import Rect

from sonos import Sonos

from ui.list_view import ListView
from ui.navigation_scene import NavigationScene
from ui.window import Window

from scenes.select_track import SelectTrack

import ui.colors as colors


class SelectAlbum(NavigationScene):
    def __init__(self, sonos, title="Albums", albums=None):
        NavigationScene.__init__(self, title)


        self.sonos = sonos
        self.background_color = colors.NAVY        

        if albums == None:
            albums = Sonos.albums()
        self.albums = albums
        self.album_titles = []
        for album in self.albums:
            self.album_titles.append(album.title)       

        # Add list of albums
        self.album_list_view = ListView(Rect(0,80,Window.frame.width, Window.frame.height - 80),self.album_titles)
        self.album_list_view.on_selected.connect(self.album_selected)
        self.add_child(self.album_list_view)

        
    def album_selected(self, list_view, title, index):
        # Browse the tracks for this album        
        scene = SelectTrack(self.sonos,title,Sonos.browse(self.albums[index]),self.albums[index])
        self.add_child(scene)
        