import pygame
import os

# Environment Vars
IMAGE_FOLDER_PATH = os.getenv('IMAGE_FOLDER_PATH')

class Image:
    """Helper class to load images using pygame

    Example: self.image = Image("test", "play_track.png")
    """
    
    def __init__(self, name, file_name):
        self.name = name
        self.surface = None        
        try:
            self.surface = pygame.image.load(IMAGE_FOLDER_PATH + file_name)
        except:
            pass
