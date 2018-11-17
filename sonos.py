# Supress future warning for SoCo
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import soco
from soco.events import event_listener

from threading import Thread

class Sonos(object):
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
        self._current_zone = Sonos._getZoneByName(zoneName)

    
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
    
    def listenForZoneChanges(self, callback):
        self._listeningForZoneChanges = True
        self._avTransportSubscription = self._current_zone.avTransport.subscribe()
        self._renderingControlSubscription = self._current_zone.renderingControl.subscribe()

        def listen():
            while self._listeningForZoneChanges:
                try:
                    event = self._avTransportSubscription.events.get(timeout=0.5)                    
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

    def stopListeningForZoneChanges(self, callback):
        self._listeningForZoneChanges = False
        self._zoneListenerThread.join()
        callback()

    @staticmethod
    def getZoneNames():
        zone_list = list(soco.discover())
        zone_names = []    
        for zone in zone_list:
            zone_names.append(zone.player_name)
        return zone_names

    ### Private Methods ###
    @staticmethod
    def _getZoneByName(zoneName):
        '''Returns a SoCo instance if found, or None if not found'''
        zone_list = list(soco.discover())        
        for zone in zone_list:
            if zone.player_name == zoneName:
                return zone
                
        return None