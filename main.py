import pygame
import os
from time import sleep

#Colours
WHITE = (255,255,255)

os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode()
lcd.fill((0,0,0))
pygame.display.update()

font_big = pygame.font.Font(None, 100)

while True:
    text_surface = font_big.render('Hello World', True, WHITE)
    rect = text_surface.get_rect(center=(240,160))
    lcd.blit(text_surface, rect)
    pygame.display.update()
    sleep(0.1)
