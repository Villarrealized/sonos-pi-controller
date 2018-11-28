from pygame import Rect

from sonos import Sonos

from ui.image import Image
from ui.button import Button
from ui.list_view import ListView
from ui.navigation_scene import NavigationScene
from ui.window import Window

import ui.colors as colors


class SelectTrack(NavigationScene):
    def __init__(self, sonos, title, tracks, playlist):
        NavigationScene.__init__(self, title)

        self.sonos = sonos
        self.background_color = colors.NAVY

        self.tracks = tracks
        self.track_titles = []
        self.playlist = playlist
        for track in self.tracks:
            self.track_titles.append(track.title)       

        # Add list of tracks
        self.track_list_view = ListView(Rect(0,80,Window.frame.width, Window.frame.height - 80),self.track_titles)
        self.track_list_view.on_selected.connect(self.track_selected)
        self.add_child(self.track_list_view)

        ##### Play All Button #####
        play_all_button_image = Image('play_all_button',filename='play_all.png')
        self.play_all_button = Button(Rect(30,self.frame.height - 55,30,30),image=play_all_button_image)        
        self.play_all_button.on_tapped.connect(self.play_all)        
        self.add_child(self.play_all_button)

        ##### Shuffle Button #####
        shuffle_button_image = Image('shuffle_button',filename='shuffle.png')
        self.shuffle_button = Button(Rect(250,self.frame.height - 60,40,40),image=shuffle_button_image)        
        self.shuffle_button.on_tapped.connect(self.shuffle)        
        self.add_child(self.shuffle_button) 
        
        
    def track_selected(self, list_view, title, index):                
        self.sonos.play_track(self.tracks[index])
        self.popToMainScene()

    def play_all(self, button):
        self.sonos.play_mode = 'NORMAL'
        self.sonos.play_playlist(self.playlist)
        self.popToMainScene()

    def shuffle(self, button):
        self.sonos.play_mode = 'SHUFFLE_NOREPEAT'
        self.sonos.play_playlist(self.playlist)
        self.popToMainScene()
        