import os
import pygame
from time import sleep

from signal import alarm, signal, SIGALRM, SIGKILL

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

print "Initializing..."
init_Pygame()

print "hiding mouse"
pygame.mouse.set_visible(False)
print "filling screen with black"
lcd.fill((0,0,0))
print "updating screen"
pygame.display.update()

font_big = pygame.font.Font(None, 100)

print "entering main loop...."
while True:
    text_surface = font_big.render('Hello World', True, WHITE)
    rect = text_surface.get_rect(center=(240,160))
    lcd.blit(text_surface, rect)
    pygame.display.update()    
    sleep(0.1)    
