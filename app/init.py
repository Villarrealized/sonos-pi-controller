from signal import alarm, signal, SIGALRM, SIGKILL

import pygame

from controller.device.backlight import Backlight
from controller.ui import color
# return the pygame screen
def init_pygame():
    backlight = Backlight()
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
        print ("getting lcd")
        lcd = pygame.display.set_mode()
        # Hide the mouse
        pygame.mouse.set_visible(False)        
        # Set the background color and turn on display
        backlight.on()
        
        lcd.fill(color.NAVY)
        pygame.display.update()

        font_big = pygame.font.Font(None, 25)
        text_surface = font_big.render('Tap to pause/play music in TV Room', True, color.WHITE)
        rect = text_surface.get_rect(center=(160,240))
        lcd.blit(text_surface, rect)

        text = font_big.render('Test', True, color.WHITE)
        rect = pygame.Rect(0,0,100,30)
        lcd.blit(text, rect)


        pygame.display.update()

        alarm(0)
        return lcd
    except Alarm:
        raise KeyboardInterrupt