import os
from signal import signal, SIGINT, SIGTERM
import sys
from time import sleep
from threading import Timer

import pygame
from pygame.locals import MOUSEBUTTONUP

from sonos import Sonos

# import project files
import ui as ui
from ui.window import Window
import ui.colors as colors
from device.backlight import Backlight
from scenes.now_playing import NowPlaying

# Handle Terminate signal, exit gracefully.
def exit_handler(sig, frame):
    print ("Exiting app...")
    Window.scene = None
    Window.surface.fill(colors.BLACK)
    pygame.display.update()

    Backlight.off()
    pygame.quit()
    sys.exit(0)

# Register signals for when app is interrupted or terminated
signal(SIGINT, exit_handler)
signal(SIGTERM, exit_handler)


########## MAIN LOOP ###########
# Initialize UI window
ui.init()

sonos = Sonos()
# Set the scene here
now_playing = NowPlaying(sonos)
Window.scene = now_playing

BACKLIGHT_TIMEOUT = int(os.getenv('BACKLIGHT_TIMEOUT'))
backlight_timer = Timer(BACKLIGHT_TIMEOUT, Backlight.off)
backlight_timer.start()


touch_enabled = True
def enable_touch():
    global touch_enabled
    touch_enabled = True

def start_backlight_timer():
    global backlight_timer
    if not backlight_timer.is_alive():                    
        backlight_timer = Timer(BACKLIGHT_TIMEOUT, Backlight.off)
        backlight_timer.start()        

def wake_up_display():  
    ''' Turn display on and prevent accidental touch by disabling touch for 0.5 seconds '''  
    global touch_enabled 
    Backlight.on()
    touch_enabled = False
    timer = Timer(0.5, enable_touch)
    timer.start()


 ##### Main Loop #####
while True:    
    # Scan touchscreen events
    for event in pygame.event.get():
        mouse_position = pygame.mouse.get_pos()        

        # print ""
        # print ("Tap on window at: {}".format(mouse_position))               

        if Backlight.enabled:
            if touch_enabled:
                # Cancel the timer any time the screen is touched        
                backlight_timer.cancel()
                # Process touch events
                hit_view = Window.scene.hit(mouse_position)        
                if event.type is MOUSEBUTTONUP:
                    start_backlight_timer()
                    if hit_view is not None and hit_view is not Window.scene:
                        hit_view.mouse_up(event.button, mouse_position)                                        
        else:            
            # Turn the backlight on if the screen has been touched
            wake_up_display()
            # This is necessary to turn display off if 
            # the screen is not touched after the initial wakeup touch
            start_backlight_timer()                
                   

    Window.update()

    # Return time to CPU to not hog resources during loop
    sleep(0.02)


    