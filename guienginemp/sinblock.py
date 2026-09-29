import pygame
import math
import time
from .baseobj import BaseObj

class sinBlock(BaseObj):
    def __init__(self, root, argDict):
        super(sinBlock, self).__init__()
        
        self.size = (10, 10)
        self._size = None
        self.rect = pygame.rect.Rect((0, 0), self.size)
        self.light = 255
        self.start = False
        self.frequency = 5
        self.phase = 0
        self.extend_parm(["size", "light", "start", "frequency", "phase"])
        
        self.images = []
        self.reset_gray_sur(self.size)
        
        self.clk = time.time()
        self.root = root
        self.textrect = None
        self.txtsur = None
        self.reset(argDict)
    
    def reset_gray_sur(self, size):
        if size != self._size:
            self.images = []
            for i in range(256):
                sur = pygame.surface.Surface(size)
                sur.fill((i, i, i))
                self.images.append(sur)
            self.rect = pygame.rect.Rect((0, 0), size)
            self._size = size
    
    def reset(self, argDict):
        self.update_parm(argDict)
        
        self.reset_gray_sur(self.size)
        
        if self.light < 0:
            self.light = 0
        self.light %= 256
        
        if "start" in argDict and argDict["start"]:
            self.clk = time.time()
        
        setattr(self.rect, self.anchor, self.position)
        self.reset_font()
        
        if self.text != "":
            self.txtsur = self.font_object.render(self.text, 1, self.textcolor)
            text_rect = self.txtsur.get_rect()
            setattr(text_rect, self.textanchor, getattr(self.rect, self.textanchor))
            self.textrect = text_rect

    def show(self):
        if self.visible:
            if self.start:
                tt = time.time()
                t = tt - self.clk
                gs = int(
                    (math.sin(2 * math.pi * self.frequency * t + self.phase - 0.5 * math.pi) + 1) * 0.5 * self.light)
                self.root.blit(self.images[gs], self.rect)
            else:
                # 静止状态：先绘制边框（可能变红），再绘制文字
                if self.borderon:
                    pygame.draw.rect(self.root, self.bordercolor, self.rect, self.borderwidth)
                if self.txtsur is not None:
                    self.root.blit(self.txtsur, self.textrect)

    def release(self):
        pass
        return