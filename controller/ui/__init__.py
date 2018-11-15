from signal import alarm, signal, SIGALRM

import pygame

from controller.device.backlight import Backlight
from window import Window

def init():
    # setup window
    Window.frame = pygame.Rect(0,0,320,480)    

    ####################
    # this section is an unbelievable nasty hack - for some reason Pygame
    # needs a keyboardinterrupt to initialise in some limited circs    

    class Alarm(Exception):
        pass
    
    def alarm_handler(signum, frame):
        raise Alarm

    signal(SIGALRM, alarm_handler)
    alarm(3)
    try:
        pygame.init()
        Window.surface = pygame.display.set_mode(Window.frame.size,pygame.FULLSCREEN)        
        alarm(0)
    except Alarm:
        raise KeyboardInterrupt
    ##################
    # Hide the mouse
    pygame.mouse.set_visible(False) 

    # Turn on backlight
    Backlight.on()