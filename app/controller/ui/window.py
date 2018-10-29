import pygame

class Window:
    """ Everything is drawn to the window. Only need 1 instance. Should never change."""
    # A Scene is a View that fills the entire screen and can be changed
    scene = None
    # the bounds of the window
    frame = None
    # pygame Surface used to draw on
    # holds result of pygame.display.set_mode()
    surface = None

    @staticmethod
    def update():
        if Window.scene is not None:
            Window.scene.draw()
            Window.surface.blit(Window.scene.surface, (0,0))
            pygame.display.update()
    
        

        