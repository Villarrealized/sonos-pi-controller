import os
import signal
import sys
from time import sleep
import pygame
from pygame.locals import *
import pygameui
import requests

from init import init_pygame

API_URL = os.getenv('API_URL')
BACKLIGHT_CONTROL = os.getenv('BACKLIGHT_CONTROL')

# Turn the backlight on
with open(BACKLIGHT_CONTROL, 'w') as f:
    f.write('1')

lcd = init_pygame()

#Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
NAVY = (11,64,109)

pygame.mouse.set_visible(False)
lcd.fill(NAVY)
pygame.display.update()

font_big = pygame.font.Font(None, 30)
text_surface = font_big.render('Tap to pause/play music in TV Room', True, WHITE)
rect = text_surface.get_rect(center=(240,160))
lcd.blit(text_surface, rect)
pygame.display.update()

playing = False


def exit_app(sig, frame):
    print "Clearing screen..."
    lcd.fill(BLACK)
    pygame.display.update()
    print "Turning off backlight..."
    with open(BACKLIGHT_CONTROL, 'w') as f:
                f.write('0')
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
    sleep(0.1)


    