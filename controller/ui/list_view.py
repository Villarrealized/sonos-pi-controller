import pygame

from view import View
from callback_signal import Signal


class ListView(View):
    """Vertical list of tappable items
    Signals
        on_selected(list_view, item, index)
            item clicked
    """

    def __init__(self, frame, items, **kwargs):
        frame.size = self._find_size_to_contain(items)
        View.__init__(self, frame)

        self.items = items 
        self.on_selected = Signal()

        self.font_size = 24
        self.item_padding = 30

        for key, value in kwargs.items():
            if key == 'font_size':
                self.font_size = value
            if key == 'item_padding':
                self.item_padding = value           

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, new_items):
        for child in self.children:
            child.rm()

        w, h = 0, 0
        for item in new_items:
            item.frame.topleft = (0, h)
            self.add_child(item)
            w = max(w, item.frame.w)
            h += item.frame.h
        self.frame.size = (w, h)

        self._items = new_items

        if self.parent is not None:
            self.layout()

    def _find_size_to_contain(self, items):
        w, h = 0, 0
        for item in items:
            w = max(w, item.frame.w)
            h += item.frame.h
        return (w, h)

    def select(self, index):        
        if index is not None:
            item = self.items[index]
            self.on_selected(self, item, index)

    def mouse_up(self, button, point):
        for index, child in enumerate(self.children):
            if point[1] >= child.frame.top and point[1] <= child.frame.bottom:
                self.select(index)
                break