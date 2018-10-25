from signal import alarm, signal, SIGALRM, SIGKILL
import pygame
# return the pygame screen
def init_pygame():
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
        return lcd
    except Alarm:
        raise KeyboardInterrupt