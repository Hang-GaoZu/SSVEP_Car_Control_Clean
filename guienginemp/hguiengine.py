import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
import time
from pygame.locals import *
try:
    from .block import Block
    from .sinblock import sinBlock
except ImportError:
    from .block import Block
    from .sinblock import sinBlock

# 安全的 get_refresh_rate 替代（如果 getfps 模块损坏或缺失）
try:
    from .getfps import get_refresh_rate
except ImportError:
    def get_refresh_rate():
        """返回显示器刷新率，失败则返回 60"""
        try:
            from screeninfo import get_monitors
            mons = get_monitors()
            for m in mons:
                if m.is_primary and m.refresh_rate:
                    return int(m.refresh_rate)
            return 60
        except:
            return 60

from typing import final
import threading

def mirror(info):
    print("[%.9f]%s" % (time.time(), info))

class HGuiEngine(threading.Thread):
    def __init__(self, stims):
        self.stimuli = {}
        pygame.init()
        pygame.font.init()
        self.running = True
        self.lock = threading.RLock()

        # 窗口模式设置
        screen_type = stims["screen"]["type"].lower()
        if screen_type == "fullscreen":
            self.screen = pygame.display.set_mode((0, 0), FULLSCREEN)
        elif screen_type == "frameless":
            self.screen = pygame.display.set_mode(stims["screen"]["size"], NOFRAME)
        else:
            self.screen = pygame.display.set_mode(stims["screen"]["size"])

        self.screen_color = stims["screen"]["color"]
        self.screen.fill(self.screen_color)
        pygame.display.set_caption(stims["screen"]["caption"])

        # FPS 设置（修复原逻辑错误）
        if "Fps" in stims["screen"]:
            self.Fps = stims["screen"]["Fps"]
        else:
            self.Fps = get_refresh_rate()
        if self.Fps <= 0:
            self.Fps = 60

        # 创建刺激对象
        del stims["screen"]
        for ID in stims:
            element = stims[ID]
            cls = element["class"]
            print(f"\n[hguiengine] 创建刺激对象: {ID}, class={cls}")
            print(f"  参数: {element['parm']}")
            if cls == "Block":
                self.stimuli[ID] = Block(self.screen, element["parm"])
            elif cls == "sinBlock":
                self.stimuli[ID] = sinBlock(self.screen, element["parm"])
            print(f"[hguiengine] {ID} 创建完成\n")

        super().__init__()
        self.daemon = True

    def currentStep(self):
        """子类覆盖此方法实现自定义控制逻辑"""
        with self.lock:
            time.sleep(1)

    def stopExp(self):
        self.running = False

    def run(self):
        while self.running:
            self.currentStep()

    @final
    def mainLoop(self):
        self.start()
        mirror("[guiengine] start")
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            self.screen.fill(self.screen_color)
            with self.lock:
                # 按 layer 排序后绘制
                for _, stim in sorted(self.stimuli.items(), key=lambda x: x[1].layer):
                    stim.show()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.running = False
            clock.tick(self.Fps)

        pygame.quit()
        for stim in self.stimuli.values():
            stim.release()
        mirror("[guiengine] exit!")