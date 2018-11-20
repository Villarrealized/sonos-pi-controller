# Supress future warning for SoCo
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import soco
from soco.events import event_listener

from threading import Thread

class Sonos(object):

    # The amount the volume is changed
    # each time it is increased or decreased
    VOLUME_CHANGE = 2

    def __init__(self):        
        self._current_zone = None
        self._zoneListenerThread = None
        self._renderingControlSubscription = None        
        self._avTransportSubscription = None
        self._listeningForZoneChanges = False        


    @property
    def current_zone(self):
        if self._current_zone is not None:            
            return self._current_zone.player_name

        return None

    @current_zone.setter
    def current_zone(self, zoneName):
        if self._current_zone is not None and self._current_zone.player_name != zoneName:
            # Stop listening for zone changes first
            self.stop_listening_for_zone_changes()
            # Change zone
            self._current_zone = Sonos.get_zone_by_name(zoneName)
        else:
            # Change zone
            self._current_zone = Sonos.get_zone_by_name(zoneName)
        

    
    @property
    def mute(self):
        if self._current_zone is not None:
            return self._current_zone.mute

    @mute.setter
    def mute(self, mute):
        if self._current_zone is not None:
            self._current_zone.mute = mute

    @property
    def volume(self):
        if self._current_zone is not None:
            return self._current_zone.volume

    @volume.setter
    def volume(self, volume):
        if self._current_zone is not None:
            self._current_zone.volume = volume

    
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
    
    def listen_for_zone_changes(self, callback):
        self._listeningForZoneChanges = True
        self._avTransportSubscription = self._current_zone.avTransport.subscribe()
        self._renderingControlSubscription = self._current_zone.renderingControl.subscribe()

        def listen():
            while self._listeningForZoneChanges:
                try:
                    event = self._avTransportSubscription.events.get(timeout=0.5)
                    # Add in track info as well     
                    event.variables['track'] = self._current_zone.get_current_track_info()       
                    callback(event.variables)
                except:
                    pass
                try:
                    event = self._renderingControlSubscription.events.get(timeout=0.5)
                    callback(event.variables)
                except:
                    pass
            
            self._avTransportSubscription.unsubscribe()
            self._renderingControlSubscription.unsubscribe()
            event_listener.stop()
            
        self._zoneListenerThread = Thread(target=listen)
        self._zoneListenerThread.start()

    def stop_listening_for_zone_changes(self, callback=None):
        self._listeningForZoneChanges = False
        if self._zoneListenerThread is not None: self._zoneListenerThread.join()
        if callback: callback()        

    @staticmethod
    def get_zone_names():
        zone_list = list(soco.discover())
        zone_names = []    
        for zone in zone_list:
            zone_names.append(zone.player_name)
        return sorted(zone_names)

    ### Private Methods ###
    @staticmethod
    def get_zone_by_name(zoneName):
        '''Returns a SoCo instance if found, or None if not found'''
        zone_list = list(soco.discover())        
        for zone in zone_list:
            if zone.player_name == zoneName:
                return zone
                
        return None