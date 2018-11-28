from pygame import Rect

from sonos import Sonos

from ui.list_view import ListView
from ui.navigation_scene import NavigationScene
from ui.window import Window

import ui.colors as colors


class SelectTrack(NavigationScene):
    def __init__(self, sonos, title, tracks):
        NavigationScene.__init__(self, title)

        self.sonos = sonos
        self.background_color = colors.NAVY        

        self.tracks = tracks
        self.track_titles = []
        for track in self.tracks:
            self.track_titles.append(track.title)       

        # Add list of tracks
        self.track_list_view = ListView(Rect(0,80,Window.frame.width, Window.frame.height - 80),self.track_titles)
        self.track_list_view.on_selected.connect(self.track_selected)
        self.add_child(self.track_list_view)

        
    def track_selected(self, list_view, title, index):        
        print(self.tracks[index])
        print(vars(self.track[index]))
        # self.sonos.play_track(self.tracks[index])
        # self.popToMainScene()