import os

BACKLIGHT_CONTROL = os.getenv('BACKLIGHT_CONTROL')

class Backlight:
    def __init__(self):
        # Get the current state
        with open(BACKLIGHT_CONTROL) as file:
            self.enabled = bool(int(file.read()))                 
        # turn on backlight
        self.on()
    
    def on(self):
        if not self.enabled:
            print "Turning display on"
            with open(BACKLIGHT_CONTROL, 'w') as file:
                file.write('1')
            self.enabled = True
    def off(self):
        print(self.enabled)
        if self.enabled:
            print "Turning display off"
            with open(BACKLIGHT_CONTROL, 'w') as file:
                file.write('0')
            self.enabled = False