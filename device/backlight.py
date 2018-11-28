import os

BACKLIGHT_CONTROL = os.getenv('BACKLIGHT_CONTROL')

class Backlight:
    """Static Class for controlling device backlight"""
    # Get the current state
    with open(BACKLIGHT_CONTROL) as file:
        enabled = bool(int(file.read()))

    @staticmethod
    def on():
        if not Backlight.enabled:            
            with open(BACKLIGHT_CONTROL, 'w') as file:
                file.write('1')
            Backlight.enabled = True
            
    @staticmethod
    def off():
        if Backlight.enabled:            
            with open(BACKLIGHT_CONTROL, 'w') as file:
                file.write('0')
            Backlight.enabled = False
        