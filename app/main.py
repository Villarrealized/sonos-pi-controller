import os
import signal
import sys
from time import sleep

import pygame
from pygame.locals import *
from init import init_pygame
import pygameui as ui
import requests

# import project files
import color
from backlight import Backlight
from ui.main_scene import MainScene

# Environment Vars
API_URL = os.getenv('API_URL')

# Global Vars
lcd = None
playing = False
backlight = Backlight()

# Handle Terminate signal, exit gracefully.
def exit_app(sig, frame):
    print "Clearing screen..."
    lcd.fill(color.BLACK)
    pygame.display.update()

    backlight.off()
    pygame.quit()
    sys.exit(0)
    
# Register signal
signal.signal(signal.SIGINT, exit_app)
signal.signal(signal.SIGTERM, exit_app)

# Initialize pygame
lcd = init_pygame()

#Add ui
ui.init('Sonos Pi Touch',(480,320))
ui.scene.push(MainScene())
ui.run()

# print "entering main loop"
# while True:
#     # Scan touchscreen events
#     for event in pygame.event.get():
#         if(event.type is MOUSEBUTTONUP):
#             if playing:
#                 requests.post(API_URL + '/room/tv/pause')
#                 playing = False
#             else:
#                 requests.post(API_URL + '/room/tv/play')
#                 playing = True
#             pos = pygame.mouse.get_pos()
#             print pos

#     # Return time to CPU to not hog resources during loop
#     sleep(0.02)


    