import pygame
from .baseobj import BaseObj

class Block(BaseObj):
    def __init__(self, root, argDict):
        super(Block, self).__init__()
        
        self.size = (10, 10)
        self.transparent = False
        self.extend_parm(["size", "transparent"])
        
        self.root = root
        
        self.image = None
        self.rect = None
        self.textrect = None
        self.txtsur = None
        
        self.reset(argDict)
    
    def reset(self, argDict):
        self.update_parm(argDict)
        
        if self.transparent:
            self.image = None
            self.rect = pygame.rect.Rect((0, 0), self.size)
        
        else:
            self.image = pygame.surface.Surface(self.size)
            self.image.fill(self.forecolor)
            self.rect = self.image.get_rect()
        
        setattr(self.rect, self.anchor, self.position)
        self.reset_font()
        
        if self.text != "":
            self.txtsur = self.font_object.render(self.text, 1, self.textcolor)
            text_rect = self.txtsur.get_rect()
            setattr(text_rect, self.textanchor, getattr(self.rect, self.textanchor))
            self.textrect = text_rect
    
    def show(self):
        if self.visible:
            if self.image is not None:
                self.root.blit(self.image, self.rect)
            elif self.txtsur is not None:
                self.root.blit(self.txtsur, self.textrect)
            elif self.borderon:
                pygame.draw.rect(self.root, self.bordercolor, self.rect, self.borderwidth)
            return
