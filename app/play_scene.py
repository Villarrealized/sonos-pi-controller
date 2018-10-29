from controller.ui.scene import Scene
from controller.ui.image import Image
import color

class PlayScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.background_color = color.NAVY        
