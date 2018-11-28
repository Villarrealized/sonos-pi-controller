import pygame
from callback_signal import Signal

class View(object):
    """A rectangular portion of the window.
    Views may have zero or more child views contained within it. 
    """
    def __init__(self, frame = None):
        
        self.frame = frame
        self.surface = None

        self.parent = None
        self.children = []

        self.hidden = False
        self._enabled = True
        self.background_color = None

        self.on_mouse_up = Signal()
        self.on_parented = Signal()
    
    @property
    def width(self):
        if self.surface is None: 
            return None
        return self.surface.get_width()

    @property
    def height(self):
        if self.surface is None: 
            return None
        return self.surface.get_height()

    def layout(self):
        """Call to have the view layout itself.

        Subclasses should invoke this after laying out child
        views and/or updating its own frame.
        """

        self.surface = pygame.Surface(self.frame.size, pygame.SRCALPHA)

    def draw(self):
        """Do not call directly."""

        if self.hidden or self.surface is None:                        
            return False
            
        if self.background_color is not None:
            self.surface.fill(self.background_color)

        for child in self.children:
            if not child.hidden:
                child.draw()
                if not child.surface.get_locked():
                    self.surface.blit(child.surface, child.frame.topleft)

    def center(self):
        if self.parent is not None:
            self.frame.center = (self.parent.frame.w // 2, self.parent.frame.h // 2)
    
    def add_child(self, child):
        assert child is not None
        self.children.append(child)
        child.parent = self
        child.parented()

    def remove_child(self, child_to_remove):
        for index, child in enumerate(self.children):
            if child == child_to_remove:
                del self.children[index]
                break

    def remove(self):
        if self.parent is not None:
            self.parent.remove_child(self)
    
    def parented(self):
        self.on_parented()


    def to_parent(self, point):
        ''' Convert child coordinates to parent's coordinates '''
        return (point[0] + self.frame.topleft[0],
            point[1] + self.frame.topleft[1])

    def to_window(self, point):
        ''' convert point to a window's point '''
        curr = self
        while curr:
            point = curr.to_parent(point)
            curr = curr.parent
        return point

    def mouse_up(self, button, point):
        # print "Mouse up on point: {}".format(point)
        self.on_mouse_up(self, button, point)

    def hit(self, point):
        """Find the view under point given, if any."""
        if self.hidden or not self._enabled:
            return None
        
        # Use pygame collidepoint method for bounding box detection
        if not self.frame.collidepoint(point):
            return None        
        
        # Find the local coordinates of tap 
        local_point = (point[0] - self.frame.topleft[0], point[1] - self.frame.topleft[1])

        # print "Local point: {}".format(local_point)
        
        # Walk through children, starting with top most layer
        for child in reversed(self.children):
            hit_view = child.hit(local_point)
            if hit_view is not None:                
                return hit_view
        return self
        




        