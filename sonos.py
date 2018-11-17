import soco
from soco.events import event_listener

class Sonos(object):
    def __init__(self):        
        self._current_zone = None


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
        else:
            print('Error: current_zone is not set')
    
    def pause(self):
        if self._current_zone is not None:
            self._current_zone.pause()
        else:
            print('Error: current_zone is not set')

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