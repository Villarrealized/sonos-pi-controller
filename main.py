import pygame
from pygame.locals import *
import os
from time import sleep
import RPi.GPIO as GPIO
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

#Setup the GPIOs as outputs - only 4 and 17 are available
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

#Colours
WHITE = (255,255,255)

#init_Pygame()
pygame.init()
print "getting lcd"
lcd = pygame.display.set_mode() 

pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()

font_big = pygame.font.Font(None, 50)

touch_buttons = {'17 on':(80,60), '4 on':(240,60), '17 off':(80,180), '4 off':(240,180)}

for k,v in touch_buttons.items():
    text_surface = font_big.render('%s'%k, True, WHITE)
    rect = text_surface.get_rect(center=v)
    lcd.blit(text_surface, rect)

pygame.display.update()

print "entering main loop"
while True:
    # Scan touchscreen events
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            print pos
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            print pos
            #Find which quarter of the screen we're in
            x,y = pos
            if y < 160:
                if x < 240:
                    print "off"
                    GPIO.output(17, False)
                else:
                    GPIO.output(4, False)
            else:
                if x < 240:
                    print "on"
                    GPIO.output(17, True)
                else:
                    GPIO.output(4, True)
    sleep(0.1)