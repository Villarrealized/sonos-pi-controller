import os
from pprint import pprint

from pygame import Rect

from sonos import Sonos

from controller.ui.scene import Scene
from controller.ui.image import Image
from controller.ui.button import Button
from controller.ui.label import Label
from controller.ui.image_view import ImageView
from scenes.select_room import SelectRoom

import colors


class NowPlaying(Scene):
    def __init__(self, sonos):
        Scene.__init__(self)
        self.sonos = sonos
        self.sonos.current_zone = 'TV Room'        

        # Listen for all changes to the current zone   
        self.sonos.listen_for_zone_changes(self.zone_state_changed)

        self.firstLoad = True
        self.background_color = colors.NAVY

        # Current Room   
        self.room_label = Label(Rect(50,24,220,30),self.sonos.current_zone,30,colors.WHITE)
        self.add_child(self.room_label)

        # Select Room
        select_room_image = Image('select_room',filename='select_room.png')
        self.select_room_button = Button(Rect(270,20,30,30),image=select_room_image)
        #Touch Handler
        self.select_room_button.on_tapped.connect(self.select_room)
        self.add_child(self.select_room_button)

        # Album Art
        self.empty_album_image = Image('empty_album',filename='empty_album_art.png')
        self.album_art_view = ImageView(Rect(80,72,160,160),self.empty_album_image)
        self.add_child(self.album_art_view)

        # Track Title   
        self.track_label = Label(Rect(20,256,280,30),"",36, colors.WHITE)             
        self.add_child(self.track_label)
        # Artist
        self.artist_label = Label(Rect(20,296,280,20),"",24, colors.GRAY)
        self.add_child(self.artist_label)
        # Album
        self.album_label = Label(Rect(20,321,280,20),"",24, colors.GRAY)
        self.add_child(self.album_label)

        ##### Play Button #####
        play_track_img = Image('play_track',filename='play_track.png')
        self.play_button = Button(Rect(130,360,60,60),image=play_track_img)
        #Touch Handler
        self.play_button.on_tapped.connect(self.play)
        self.add_child(self.play_button)

        ##### Pause Button #####
        pause_track_img = Image('pause_track',filename='pause_track.png')
        self.pause_button = Button(Rect(130,360,60,60),image=pause_track_img)
        self.pause_button.hidden = True
        #Touch Handler
        self.pause_button.on_tapped.connect(self.pause)
        self.add_child(self.pause_button)

        ##### Previous Button #####
        previous_track_img = Image('previous_track',filename='previous_track.png')
        previous_track_disabled_img = Image('previous_track_disabled',filename='previous_track_disabled.png')        
        self.previous_button = Button(Rect(65,370,40,40),image=previous_track_img, disabled_image=previous_track_disabled_img)
        #Touch Handler
        self.previous_button.on_tapped.connect(self.previous)
        self.add_child(self.previous_button)

        ##### Next Button #####
        next_track_img = Image('next_track',filename='next_track.png')
        next_track_disabled_img = Image('next_track_disabled',filename='next_track_disabled.png')
        self.next_button = Button(Rect(215,370,40,40),image=next_track_img,disabled_image=next_track_disabled_img)
        #Touch Handler
        self.next_button.on_tapped.connect(self.next)
        self.add_child(self.next_button)

        ##### Volume Down Button #####
        volume_down_img = Image('volume_down',filename='volume_down.png')
        self.volume_down_button = Button(Rect(92,438,30,30),image=volume_down_img)
        #Touch Handler
        self.volume_down_button.on_tapped.connect(self.volume_down)
        self.add_child(self.volume_down_button)

        ##### Volume On Button #####
        volume_on_img = Image('volume_on',filename='volume_on.png')
        self.volume_on_button = Button(Rect(147,440,26,26),image=volume_on_img)
        #Touch Handler
        self.volume_on_button.on_tapped.connect(self.mute)
        self.add_child(self.volume_on_button)

        ##### Volume Mute Button #####
        volume_mute_img = Image('volume_mute',filename='volume_mute.png')
        self.volume_mute_button = Button(Rect(147,440,26,26),image=volume_mute_img)
        self.volume_mute_button.hidden = True
        #Touch Handler
        self.volume_mute_button.on_tapped.connect(self.unmute)
        self.add_child(self.volume_mute_button)

        # Volume Level Label
        self.volume_label = Label(Rect(30,447,40,30),"",20, colors.GRAY)
        self.add_child(self.volume_label)

        ##### Volume Up Button #####
        volume_up_img = Image('volume_up',filename='volume_up.png')    
        self.volume_up_button = Button(Rect(197,438,30,30),image=volume_up_img)
        #Touch Handler
        self.volume_up_button.on_tapped.connect(self.volume_up)
        self.add_child(self.volume_up_button)

        # Layout the scene
        self.layout()

        # Keep hidden until everything has loaded
        self.hidden = True
                     

    
    ###### Button Handlers #####
    def play(self, button):        
        # Technically, we don't need to call this here, but it helps with 
        # the UI responsiveness, so we don't need to wait for the listener to respond
        self.update_play_pause('PLAYING')
        self.sonos.play()

    def pause(self, button):
        self.update_play_pause('PAUSED_PLAYBACK')
        self.sonos.pause()
    
    def next(self, button):
        self.sonos.next()

    def previous(self, button):
        self.sonos.previous()

    def volume_down(self, button):        
        new_volume = str(int(self.volume_label.text.replace('%','')) - Sonos.VOLUME_CHANGE)
        self.volume_label.text = new_volume + "%"
        self.sonos.volume -= Sonos.VOLUME_CHANGE
        
    def volume_up(self, button):        
        new_volume = str(int(self.volume_label.text.replace('%','')) + Sonos.VOLUME_CHANGE)
        self.volume_label.text = new_volume + "%"
        self.sonos.volume += Sonos.VOLUME_CHANGE

    def mute(self, button):        
        self.update_volume_state(1)
        self.sonos.mute = 1
    
    def unmute(self, button):
        self.update_volume_state(0)
        self.sonos.mute = 0

    def select_room(self, button):
        # Modal
        self.selectRoomScene = SelectRoom(self.sonos)        
        self.add_child(self.selectRoomScene)             

    ##### End Button Handlers #####

    def change_room(self, room):
        if self.sonos.current_zone != room:
            self.sonos.current_zone = room
            self.room_label.text = room
            # Subscribe to new zone changes
            self.sonos.listen_for_zone_changes(self.zone_state_changed)

    def show_ui(self):
        for child in self.children:
            child.hidden = False

    def update_volume_state(self, mute):
        if mute:
            self.volume_on_button.hidden = True
            self.volume_mute_button.hidden = False
        else:
            self.volume_on_button.hidden = False
            self.volume_mute_button.hidden = True

    def update_volume_label(self, volume):        
        self.volume_label.text = str(volume) + "%"

    def update_play_pause(self, state):        
        if state == 'PLAYING':
            self.play_button.hidden = True
            self.pause_button.hidden = False
        elif state == 'PAUSED_PLAYBACK' or state == 'STOPPED':
            self.play_button.hidden = False
            self.pause_button.hidden = True

    def update_available_actions(self, actions):        
        self.next_button.enabled = 'Next' in actions
        self.previous_button.enabled = 'Previous' in actions

    def update_track_info(self,track):
        # print('Duration: {}'.format(track['duration']))
        # print('Position: {}'.format(track['position']))

        self.track_label.text = track['title']
        self.artist_label.text = track['artist']
        self.album_label.text = track['album']

        # Only set the image if it has changed
        if self.album_art_view.image.name != self.album_label.text:
            # Set album art to the url given if it is not empty, otherwise use the default image
            if track['album_art'].strip() != "":                     
                self.album_art_view.image = Image(self.album_label.text,image_url=track['album_art'])            
            else:
                self.album_art_view.image = self.empty_album_image        

    def zone_state_changed(self, data):
        '''Callback function that is called every time the zone state changes ex. new track, play, pause, volume change, etc.'''        
        # print("")
        # pprint(data)
        # print("")                        

        # Handle all the changed data
        if 'current_transport_actions' in data: self.update_available_actions(data['current_transport_actions'].split(', '))
        if 'transport_state' in data: self.update_play_pause(data['transport_state'])
        if 'track' in data: self.update_track_info(data['track'])
        if 'mute' in data: self.update_volume_state(int(data['mute']['Master']))        
        if 'volume' in data: self.update_volume_label(int(data['volume']['Master']))        
        
        # Reveal UI after we have loaded the data for the first time
        if self.firstLoad:  
            self.hidden = False
            self.firstLoad = False  

        
       