from pygame import Rect

from sonos import Sonos

from ui.list_view import ListView
from ui.navigation_scene import NavigationScene
from ui.window import Window

from scenes.select_track import SelectTrack

import ui.colors as colors


class SelectPlaylist(NavigationScene):
    def __init__(self, sonos, playlists=Sonos.playlists()):
        NavigationScene.__init__(self, "Playlists")


        self.sonos = sonos
        self.background_color = colors.NAVY        

        self.playlists = playlists
        self.playlist_titles = []
        for playlist in self.playlists:
            self.playlist_titles.append(playlist.title)       

        # Add list of playlists
        self.playlist_list_view = ListView(Rect(0,80,Window.frame.width, Window.frame.height - 80),self.playlist_titles)
        self.playlist_list_view.on_selected.connect(self.playlist_selected)
        self.add_child(self.playlist_list_view)

        
    def playlist_selected(self, list_view, title, index):
         # Browse the tracks for this playlist
        scene = SelectTrack(self.sonos,title,Sonos.browse(self.playlists[index]))
        self.add_child(scene)