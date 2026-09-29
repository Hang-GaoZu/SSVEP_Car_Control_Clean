import pygame
import os

_font_path = os.path.join(os.path.dirname(__file__), "msyh.ttc")

def get_ch_fonts():
    candidate_fonts = ["microsoftyahei", "simsun", "simhei", "kaiti", "fangsong"]
    try:
        system_fonts = pygame.font.get_fonts()
        available_fonts = [font for font in candidate_fonts if font.lower() in system_fonts]
        return available_fonts
    except (TypeError, Exception) as e:
        print(f"获取系统字体失败: {e}，使用Windows系统字体路径")
        return []

class BaseObj(pygame.sprite.Sprite):
    def __init__(self):
        super(BaseObj, self).__init__()
        
        self.position = (0, 0)
        self.anchor = "center"
        self.forecolor = (255, 255, 255)
        
        self.borderon = False
        self.borderwidth = 2
        self.bordercolor = (255, 0, 0)
        
        self.textcolor = (0, 255, 0)
        self.textanchor = "center"
        self.textsize = 10
        self._textsize = 10
        self.text = ""
        
        self.layer = 0
        self.visible = False
        
        self.parmkeys = ["position", "anchor", "forecolor", "borderon", "borderwidth", "bordercolor", "textcolor", "textanchor", "textsize", "text", "layer", "visible"]
        
        self.ch_fonts = get_ch_fonts()
        self.reset_font()
    
    def extend_parm(self, parm):
        self.parmkeys.extend(parm)
    
    def reset_font(self):
        font_loaded = False
        
        if len(self.ch_fonts) > 0:
            try:
                self.font_object = pygame.font.SysFont(self.ch_fonts[0], int(self.textsize))
                print(f"使用系统中文字体: {self.ch_fonts[0]}, 大小: {self.textsize}")
                font_loaded = True
                return
            except Exception as e:
                print(f"系统字体加载失败: {e}")
        
        if not font_loaded:
            try:
                if os.path.exists(_font_path):
                    self.font_object = pygame.font.Font(_font_path, int(self.textsize))
                    print(f"使用本地字体文件: {_font_path}, 大小: {self.textsize}")
                    font_loaded = True
                    return
                else:
                    print(f"本地字体文件不存在: {_font_path}")
            except Exception as e:
                print(f"本地字体加载失败: {e}")
        
        if not font_loaded:
            windows_fonts = [
                r"C:\Windows\Fonts\msyh.ttc",
                r"C:\Windows\Fonts\simhei.ttf",
                r"C:\Windows\Fonts\simsun.ttc",
                r"C:\Windows\Fonts\simkai.ttf",
            ]
            
            for font_path in windows_fonts:
                try:
                    if os.path.exists(font_path):
                        self.font_object = pygame.font.Font(font_path, int(self.textsize))
                        print(f"使用Windows系统字体: {font_path}, 大小: {self.textsize}")
                        font_loaded = True
                        break
                except Exception as e:
                    print(f"字体 {font_path} 加载失败: {e}")
                    continue
            
            if font_loaded:
                return
        
        if not font_loaded:
            try:
                self.font_object = pygame.font.SysFont("arial", int(self.textsize))
                print(f"使用Arial字体(仅支持英文), 大小: {self.textsize}")
                font_loaded = True
            except Exception as e:
                print(f"Arial字体加载失败: {e}")
                self.font_object = pygame.font.Font(None, int(self.textsize))
                print(f"使用pygame基础字体(不支持中文), 大小: {self.textsize}")

    def update_parm(self, argDict):
        for key in argDict:
            if key in self.parmkeys:
                if key in ("anchor", "textanchor"):
                    if argDict[key] in ("topleft", "bottomleft", "topright",
                                        "bottomright", "midtop", "midleft",
                                        "midbottom", "midright", "center"):
                        setattr(self, key, argDict[key])
                else:
                    setattr(self, key, argDict[key])
    
    def reset(self, argDict):
        pass
    
    def show(self):
        pass
    
    def release(self):
        pass
