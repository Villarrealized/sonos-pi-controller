import pygame

from view import View

class ImageView(View):
    """A view for displaying an image.
    The only 'content scaling mode' currently supported is 'scale-to-fill'.
    """

    def __init__(self, frame, image):
        """Create an image view from an image.
        frame.topleft
            where to position the view.
        frame.size
            if (0, 0) the frame.size is set to the image's size;
            otherwise, the image is scaled to this size.
        """

        assert image is not None

        if frame is None:
            frame = pygame.Rect((0, 0), image.get_size())
        elif frame.w == 0 and frame.h == 0:
            frame.size = image.get_size()

        View.__init__(self, frame)

        self._enabled = False
        self.image = image

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, new_image):
        self._image = new_image
        self.layout()

    def layout(self):
        self._image.surface = pygame.transform.smoothscale(self._image.surface, self.frame.size).convert()        

    def draw(self):
        self.surface = self._image.surface