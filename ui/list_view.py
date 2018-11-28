from pygame import Rect

from ui.view import View
from ui.image import Image
from ui.button import Button
from ui.label import Label
from ui.callback_signal import Signal

import ui.colors as colors


class ListView(View):
    
    ''' The ListView is a reusable view for displaying paged lists of items

    Items is an array of strings that will be made into a list of buttons'''
    def __init__(self, frame, items):
        View.__init__(self, frame)

        self.items = items
        self.list_buttons = []
        self.list_index = 0
        self.per_page = 7          

        self.on_selected = Signal()

        ##### Previous Button #####
        previous_button_image = Image('previous_button',filename='previous_button.png')
        self.previous_button = Button(Rect(110,self.frame.height - 60,40,40),image=previous_button_image)        
        self.previous_button.on_tapped.connect(self.previous)
        self.previous_button.hidden = True
        self.add_child(self.previous_button)

        ##### Next Button #####
        next_button_image = Image('next_button',filename='next_button.png')
        self.next_button = Button(Rect(170,self.frame.height - 60,40,40),image=next_button_image)        
        self.next_button.on_tapped.connect(self.next)
        self.next_button.hidden = True
        self.add_child(self.next_button)

        self.layout()

        self.create_items()


    def create_items(self):
        # Clean up any old buttons before addings new ones
        for button in self.list_buttons:
            button.remove()

        self.update_list_navigation()        
        y = 0
        for index, item in enumerate(self.items):
            if index >= self.list_index and index < (self.list_index + self.per_page):
                item_button = Button(Rect(40,y,240,30), 30, Label.LEFT, text=item)
                item_button.on_tapped.connect(self.select_item)
                self.add_child(item_button)
                self.list_buttons.append(item_button)
                y += 50


    def select_item(self, button):        
        self.on_selected(self, button.label.text, self.items.index(button.label.text))

    def update_list_navigation(self):
        item_count = len(self.items)
        if item_count == 0: return        

        if (self.list_index + self.per_page) < item_count:
            self.next_button.hidden = False
        else:
            self.next_button.hidden = True
        
        if (self.list_index - self.per_page) >= 0:
            self.previous_button.hidden = False
        else:
            self.previous_button.hidden = True


    def next(self, button):
        self.list_index += self.per_page
        self.create_items()

    def previous(self, button):
        self.list_index -= self.per_page
        self.create_items()

    
    def select(self, index):
        if index is not None:
            item = self.items[index]
            self.on_selected(self, item, index)

    def parented(self):
        # This is needed or else font will appear a bit fuzzy
        self.background_color = self.parent.background_color      


