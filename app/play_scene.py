from controller.ui.scene import Scene
from controller.ui.image import Image
from controller.ui.button import Button
from pygame import Rect
import color

class PlayScene(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.background_color = color.NAVY

        play_track_img = Image('play_track','play_track.png')
        button = Button(Rect(100,100,60,60),image=play_track_img)
        button.on_tapped(self.button_tapped)
        self.add_child(button)

    def button_tapped(self):
        print "Button was tapped"
