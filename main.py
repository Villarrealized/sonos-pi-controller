import pygame
from pygame.locals import *
import os
from time import sleep
from signal import alarm, signal, SIGALRM, SIGKILL
import requests

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
text_surface = font_big.render('Hello World', True, WHITE)
rect = text_surface.get_rect(center=(240,160))
lcd.blit(text_surface, rect)
pygame.display.update()

print "entering main loop"
while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            print "Mouse Down"
            pos = pygame.mouse.get_pos()
            print pos
        elif(event.type is MOUSEBUTTONUP):
            requests.post('http://192.168.0.73:8080/room/tv/play')
            print "Mouse Up"
            pos = pygame.mouse.get_pos()
            print pos
    sleep(0.1)