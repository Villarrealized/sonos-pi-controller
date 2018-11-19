import os
import io
from urllib2 import urlopen

import pygame


# Environment Vars
IMAGE_FOLDER_PATH = os.getenv('IMAGE_FOLDER_PATH')

class Image:
    """Helper class to load images using pygame

    Example: self.image = Image("test", filename="play_track.png")
    """
    
    def __init__(self, name, **kwargs):
        self.name = name
        self.surface = None
        self.file_name = None
        self.image_url = None

        for key, value in kwargs.items():
            if key == 'filename':                
                self.file_name = value                
            if key == 'image_url':
                self.image_url = value

        if self.file_name is not None:
            try:                
                self.surface = pygame.image.load(IMAGE_FOLDER_PATH + self.file_name)                
            except:
                pass
        elif self.image_url is not None:
            try:
                self.surface = pygame.image.load(self.image_from_url(self.image_url))
            except:
                pass

    def image_from_url(self, url):
        image_string = urlopen(url).read()
        # return the image 
        return io.BytesIO(image_string)



