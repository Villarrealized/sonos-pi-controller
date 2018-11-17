import os
from pprint import pprint

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
        print("Current Zone: {}".format(self.sonos.current_zone))
        # Listen for all changes to the current zone   
        self.sonos.listenForZoneChanges(self.zoneStateChanged)

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

        ##### Previous Button #####
        previous_track_img = Image('previous_track','previous_track.png')
        #Center bottom positioning
        self.previous_button = Button(Rect(70,343,30,30),image=previous_track_img)   
        #Touch Handler
        self.previous_button.on_tapped.connect(self.previous)
        self.add_child(self.previous_button)

        ##### Next Button #####
        next_track_img = Image('next_track','next_track.png')
        #Center bottom positioning
        self.next_button = Button(Rect(220,343,30,30),image=next_track_img)                
        #Touch Handler
        self.next_button.on_tapped.connect(self.next)
        self.add_child(self.next_button)


        


    def play(self, button):
        # Technically, we don't need to call this here, but it helps with 
        # the UI responsiveness, so we don't need to wait for the listener to respond
        self.updatePlayPause('PLAYING')
        self.sonos.play()

    def pause(self, button):
        self.updatePlayPause('PAUSED_PLAYBACK')
        self.sonos.pause()
    
    def next(self, button):
        self.sonos.next()

    def previous(self, button):
        self.sonos.previous()

    def updatePlayPause(self, state):        
        if state == 'PLAYING':
            self.play_button.hidden = True
            self.pause_button.hidden = False
        else:
            self.play_button.hidden = False
            self.pause_button.hidden = True

    def zoneStateChanged(self, data):
        print("")
        pprint(data)
        print("")
        
        '''Callback function that is called every time the zone state changes ex. new track, play, pause, volume change, etc.'''        
        if 'transport_state' in data: self.updatePlayPause(data['transport_state'])

        
       