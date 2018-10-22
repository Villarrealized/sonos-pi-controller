import pygame
from pygame.locals import *
import os
from time import sleep
from signal import alarm, signal, SIGALRM, SIGKILL
import requests

API_URL = os.getenv('API_URL')

lcd = None
def init_Pygame():
    global lcd
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
        print "getting lcd"
        lcd = pygame.display.set_mode() 
        alarm(0)
    except Alarm:
        raise KeyboardInterrupt

#Colours
WHITE = (255,255,255)

init_Pygame()

pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()

font_big = pygame.font.Font(None, 50)
text_surface = font_big.render('Tap to pause/play music in TV Room', True, WHITE)
rect = text_surface.get_rect(center=(240,160))
lcd.blit(text_surface, rect)
pygame.display.update()

playing = False

print "entering main loop"
while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONUP):
            if playing:
                requests.post(API_URL + '/room/tv/pause')
            else:
                requests.post(API_URL + '/room/tv/play')
            pos = pygame.mouse.get_pos()
            print pos
    sleep(0.1)