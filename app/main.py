import os
from signal import signal, SIGINT, SIGTERM
import sys
from time import sleep

import pygame
from pygame.locals import MOUSEBUTTONUP
import requests

# import project files
import controller.ui as ui
from controller.ui.window import Window
import color
from controller.device.backlight import Backlight
from play_scene import PlayScene

# Environment Vars
API_URL = os.getenv('API_URL')

# Global Vars
playing = False

# Handle Terminate signal, exit gracefully.
def exit_handler(sig, frame):
    print ("Exiting app...")
    Window.scene = None
    Window.surface.fill(color.BLACK)
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

# Set the scene here
play_scene = PlayScene()
Window.scene = play_scene

print ("entering main loop")
while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        mouse_position = pygame.mouse.get_pos()
        print (mouse_position) 
        if(event.type is MOUSEBUTTONUP):
            hit_view = Window.scene.hit(mouse_position)
            if hit_view is not None:
                point = hit_view(mouse_position)
                hit_view.touch_up(point)
            # if playing:
            #     requests.post(API_URL + '/room/tv/pause')
            #     playing = False
            # else:
            #     requests.post(API_URL + '/room/tv/play')
            #     playing = True                           
    Window.update()

    # Return time to CPU to not hog resources during loop
    sleep(0.02)


    