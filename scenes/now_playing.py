import os
import json
from threading import Timer
from threading import Thread

from pygame import Rect

from controller.ui.scene import Scene
from controller.ui.image import Image
from controller.ui.button import Button
from controller.ui.window import Window
import color


# Environment Vars
API_URL = os.getenv('API_URL')

class NowPlaying(Scene):
    def __init__(self, sonos):
        Scene.__init__(self)                        
        self.sonos = sonos
        self.sonos.current_zone = 'TV Room'     
        print(self.sonos.current_zone)   

        self.background_color = color.NAVY             
        ##### Play Button #####
        play_track_img = Image('play_track','play_track.png')
        #Center bottom positioning
        self.play_button = Button(Rect(130,330,60,60),image=play_track_img)
        #Touch Handler
        self.play_button.on_tapped.connect(self.play)
        self.add_child(self.play_button)

        ##### Pause Button #####
        pause_track_img = Image('pause_track','pause_track.png')
        #Center bottom positioning
        self.pause_button = Button(Rect(130,330,60,60),image=pause_track_img)
        #Hide to start
        self.pause_button.hidden = True        
        #Touch Handler
        self.pause_button.on_tapped.connect(self.pause)
        self.add_child(self.pause_button)

        self.sonos.listenForZoneChanges(self.zoneStateChanged)


    def play(self, button):
        # Technically, we don't need to call this here, but it helps with 
        # the UI responsiveness, so we don't need to wait for the listener to respond
        self.updatePlayPause('PLAYING')
        self.sonos.play()

    def pause(self, button):
        self.updatePlayPause('PAUSED_PLAYBACK')
        self.sonos.pause()

    def updatePlayPause(self, state):        
        if state == 'PLAYING':
            self.play_button.hidden = True
            self.pause_button.hidden = False
        else:
            self.play_button.hidden = False
            self.pause_button.hidden = True

    def zoneStateChanged(self, data):
        '''Callback function that is called every time the zone state changes ex. new track, play, pause, volume change, etc.'''        
        if 'transport_state' in data: self.updatePlayPause(data['transport_state'])

        
       