import os
import pygame
from time import sleep

#Colours
WHITE = (255,255,255)

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
print "Initializing..."
pygame.init()
print "hiding mouse"
pygame.mouse.set_visible(False)
print (pygame.display.get_init())
print "getting lcd"
lcd = pygame.display.set_mode()
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
    print "sleeping..."
    sleep(0.1)    
