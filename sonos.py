# Supress future warning for SoCo
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import os
from time import sleep

import soco
from soco.events import event_listener
from soco.data_structures import to_didl_string

from threading import Thread

CURRENT_ZONE_FILE=os.getenv('CURRENT_ZONE_FILE')

class Sonos(object):

    # The amount the volume is changed
    # each time it is increased or decreased
    VOLUME_CHANGE = 2
    instance = soco.discover().pop()

    def __init__(self):        
        self._current_zone = None
        self._zoneListenerThread = None
        self._renderingControlSubscription = None        
        self._avTransportSubscription = None
        self._zoneGroupTopologySubscription = None

        self._listeningForZoneChanges = False        

        self.current_zone = self.read_current_zone_file()

    # Attempts to return the current zone by reading from the setting file
    def read_current_zone_file(self):
        try:
            with open(CURRENT_ZONE_FILE) as file:                
                return file.read()
        except:
            return None

    def update_current_zone_file(self):
        try:
            with open(CURRENT_ZONE_FILE, 'w') as file:
                file.write(self.current_zone)
        except:
            pass

    @property
    def current_zone(self):
        if self._current_zone is None:                                     
            # Try to load zone from setting file
            zone = self.read_current_zone_file()            
            match = Sonos.get_zone_by_name(zone)            
            if match is not None:                                
                self._current_zone = match            
            else:
                # Set it to a random zone
                self.current_zone = soco.discover().pop().player_name          
        
        return self._current_zone.player_name   

    @current_zone.setter
    def current_zone(self, zoneName):        
        if zoneName is None or zoneName.strip() == '':
            # Set it to a random zone
            self._current_zone = soco.discover().pop()  
        elif self._current_zone is not None and self._current_zone.player_name != zoneName:
            # Stop listening for zone changes on current zone
            self.stop_listening_for_zone_changes()
            # Change zone
            self._current_zone = Sonos.get_zone_by_name(zoneName)
        else:
            self._current_zone = Sonos.get_zone_by_name(zoneName)
        
        if not self.is_coordinator:
            self.update_zone_to_coordinator()

        self.update_current_zone_file()        

    
    @property
    def mute(self):
        if self._current_zone is not None:
            return self._current_zone.mute

    @mute.setter
    def mute(self, mute):
        if self._current_zone is not None:
            self._current_zone.mute = mute

            # update group mute, if applicable
            for member in self.group_members:
                zone = Sonos.get_zone_by_name(member)
                zone.mute = mute

    @property
    def volume(self):
        if self._current_zone is not None:
            return self._current_zone.volume

    @volume.setter
    def volume(self, volume):
        if self._current_zone is not None:
            volume_diff = volume - self._current_zone.volume
            self._current_zone.volume = volume

            # update group volume, if applicable
            for member in self.group_members:
                zone = Sonos.get_zone_by_name(member)
                zone.volume += volume_diff


    @property
    def group_members(self):
        ''' Return a sorted list of unique group member names or None '''
        if self._current_zone is not None:
            unique_members = set()
            for member in self._current_zone.group.members:
                if member.player_name != self._current_zone.player_name:
                    unique_members.add(member.player_name)
                        
            return sorted(unique_members)
        return None

    @property
    def potential_members(self):
        ''' Return a sorted list of zones that COULD be or ARE a member '''
        if self._current_zone is not None:
            zones = Sonos.get_zone_names()
            # Remove this zone -- can't be a member of yourself
            zones.remove(self.current_zone)

            return zones

        return None

    @property
    def current_zone_label(self):
        ''' Return the current zone name or a modified version if there are members in its group '''
        if self._current_zone is not None:            
            num_members = len(self.group_members)            
            if num_members > 0:
                return self._current_zone.player_name + " + {}".format(num_members)
            else:
                return self._current_zone.player_name

        return ''

    @property
    def is_coordinator(self):
        if self._current_zone is not None:
            return self._current_zone.player_name == self._current_zone.group.coordinator.player_name 
        return False

    def update_zone_to_coordinator(self):
        if self._current_zone is not None:
            self.current_zone = self._current_zone.group.coordinator.player_name
    
    def play(self):
        if self._current_zone is not None:
            self._current_zone.play()
    
    def pause(self):
        if self._current_zone is not None:
            self._current_zone.pause()

    def next(self):
        if self._current_zone is not None:
            self._current_zone.next()

    def previous(self):
        if self._current_zone is not None:
            self._current_zone.pause()

    def group(self, rooms):
        ''' Joins all the speakers in the list to the current zone '''
        if self._current_zone is not None:
            for room in rooms:
                zone = Sonos.get_zone_by_name(room["name"])
                if room['join']:
                    zone.join(self._current_zone)
                else:
                    zone.unjoin()

    def play_track(self, track):
        if self._current_zone is not None:
            self._current_zone.play_uri(track.resources[0].uri, to_didl_string(track))
    
    def listen_for_zone_changes(self, callback):
        self._listeningForZoneChanges = True
        self._avTransportSubscription = self._current_zone.avTransport.subscribe()
        self._renderingControlSubscription = self._current_zone.renderingControl.subscribe()
        self._zoneGroupTopologySubscription = self._current_zone.zoneGroupTopology.subscribe()    

        def listen():
            while self._listeningForZoneChanges:                
                try:
                    event = self._avTransportSubscription.events.get(timeout=0.1)
                    # Add in track info as well     
                    event.variables['track'] = self._current_zone.get_current_track_info()
                    event.variables['tv_playing'] = int(self._current_zone.is_playing_tv)
                    callback(event.variables)
                except:
                    pass
                try:
                    event = self._renderingControlSubscription.events.get(timeout=0.1)
                    callback(event.variables)
                except:
                    pass
                try:
                    event = self._zoneGroupTopologySubscription.events.get(timeout=0.1)
                    callback(event.variables)
                except:
                    pass

            
            self._avTransportSubscription.unsubscribe()
            self._renderingControlSubscription.unsubscribe()
            self._zoneGroupTopologySubscription.unsubscribe()
            event_listener.stop()
            
        self._zoneListenerThread = Thread(target=listen)
        self._zoneListenerThread.start()

    def stop_listening_for_zone_changes(self, callback=None):
        self._listeningForZoneChanges = False
        if self._zoneListenerThread is not None: self._zoneListenerThread.join()
        if callback: callback()


    @classmethod
    def artists(cls):
        return Sonos.instance.music_library.get_artists(complete_result=True)

    @classmethod
    def albums(cls):
        return Sonos.instance.music_library.get_albums(complete_result=True)
    
    @classmethod
    def genres(cls):
        return Sonos.instance.music_library.get_genres(complete_result=True)

    @classmethod
    def playlists(cls):
        return Sonos.instance.music_library.get_playlists(complete_result=True)
    
    @classmethod
    def favorites(cls):
        return Sonos.instance.music_library.get_sonos_favorites(complete_result=True)
    
    @classmethod
    def browse(cls, ml_item):
        return Sonos.instance.music_library.browse(ml_item,0,100000,True)


                
    @staticmethod
    def get_zone_names():
        ''' Returns a sorted list of zone names '''
        zone_list = list(soco.discover())
        zone_names = []    
        for zone in zone_list:
            zone_names.append(zone.player_name)
        return sorted(zone_names)

    @staticmethod
    def get_zone_groups():
        ''' Returns a sorted list of zone groups '''
        zone_list = list(soco.discover())
        zones = []
        for zone in zone_list:
            # Set of members in group that are not itself
            unique_members = set()
            for member in zone.group.members:
                if member.player_name != zone.player_name :
                    unique_members.add(member.player_name)
            
            zones.append({
                "name": zone.player_name,
                "is_coordinator": zone.player_name == zone.group.coordinator.player_name,
                "members": sorted(unique_members) # Get sorted list from set
            })

        return sorted(zones)        

    ### Private Methods ###
    @staticmethod
    def get_zone_by_name(zoneName):
        '''Returns a SoCo instance if found, or None if not found'''
        zone_list = list(soco.discover())        
        for zone in zone_list:
            if zone.player_name == zoneName:
                return zone
                
        return None