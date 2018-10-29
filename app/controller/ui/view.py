import pygame

class View:
    """A rectangular portion of the window.
    Views may have zero or more child views contained within it. 
    """
    def __init__(self, frame = None):
        
        self.frame = frame
        self.surface = None

        self.parent = None
        self.children = []

        self.hidden = False

        self.background_color = None

        self.layout()

    def layout(self):
        """Call to have the view layout itself.

        Subclasses should invoke this after laying out child
        views and/or updating its own frame.
        """
        
        self.surface = pygame.Surface(self.frame.size, pygame.SRCALPHA)

    def draw(self):
        if self.hidden:
            return False
            
        if self.background_color is not None:
            self.surface.fill(self.background_color)

        for child in self.children:
            child.draw()
            self.surface.blit(child.surface, child.frame.topleft)

    def center(self):
        if self.parent is not None:
            self.frame.center = (self.parent.frame.w // 2, self.parent.frame.h //2)
    
    def add_child(self, child):
        assert child is not None
        self.children.append(child)
        child.parent = self

    def remove_child(self, child_to_remove):
        for index, child in enumerate(self.children):
            if child == child_to_remove:
                del self.children[index]
                break

    def remove(self):
        if self.parent is not None:
            self.parent.remove_child(self)



        