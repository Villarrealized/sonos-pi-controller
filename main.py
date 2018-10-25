import os
import signal
import sys
from time import sleep

import pygame
from pygame.locals import *
import pygameui
from init import init_pygame
import requests

# import project files
import color
from backlight import Backlight

# Environment Vars
API_URL = os.getenv('API_URL')

# Global Vars
lcd = None
playing = False
backlight = Backlight()

# Initialize pygame
lcd = init_pygame()

# Handle Terminate signal, exit gracefully.
def exit_app(sig, frame):
    print "Clearing screen..."
    lcd.fill(color.BLACK)
    pygame.display.update()
    print "Turning off backlight..."
    backlight.off()
    sys.exit(0)
# Register signal
signal.signal(signal.SIGTERM, exit_app)

print "entering main loop"
while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONUP):
            if playing:
                requests.post(API_URL + '/room/tv/pause')
                playing = False
            else:
                requests.post(API_URL + '/room/tv/play')
                playing = True
            pos = pygame.mouse.get_pos()
            print pos
    sleep(0.02)


    