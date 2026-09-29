from multiprocessing import Process, Queue
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QTimer
from mymessbox import showMessageBox
import time
import socket
import threading

from guienginemp.hguiengine import HGuiEngine

wheelcmds = {"后退": "1", "前进": "2", "左转": "3", "右转": "4", "亮灯": "5", "鸣笛": "6"}

class StiManager(QtWidgets.QDialog):
    _sig2mesbox = pyqtSignal(str)

    def __init__(self, parentUI, settings, qtsig):
        super(StiManager, self).__init__()
        self.ui = parentUI
        self.ui.bt_startssvep.clicked.connect(self.start_ssvep)
        self.ui.bt_startssvepvehicle.clicked.connect(self.start_ssvep)
        self._sig2mesbox.connect(self.popmesbox)
        self.qtsig = qtsig

        self.pgui = None
        self.que = Queue()

        scr_info = settings["scr"]
        layout_info = settings["layout"]
        self.ctrsetting = settings["ctr"]

        self.layout = {
            "screen": {
                "size": (scr_info["width"], scr_info["height"]),
                "color": (0, 0, 0),
                "Fps": scr_info["fps"],
                "caption": "ssvep demo",
                "type": scr_info["type"]
            }
        }
        for setting in layout_info:
            self.layout["sti%d" % setting["id"]] = {
                "class": "sinBlock",
                "parm": {
                    "size": (scr_info["width"] * setting["size"][0], scr_info["height"] * setting["size"][1]),
                    "position": (scr_info["width"] * setting["pos"][0], scr_info["height"] * setting["pos"][1]),
                    "anchor": "center",
                    "bordercolor": (150, 150, 150),
                    "borderon": True,
                    "borderwidth": 2,
                    "textcolor": (0, 255, 0),
                    "textanchor": "midtop",
                    "textsize": int(scr_info["height"] * setting["size"][1] * 0.25),
                    "text": setting["cmd"],
                    "layer": 1,
                    "visible": True,
                    "start": False,
                    "frequency": setting["freq"],
                    "phase": 0
                }
            }

        # 打印初始化文字信息
        print("初始化刺激块文字：")
        for i in range(6):
            print(f"  sti{i}: text='{self.layout['sti%d'%i]['parm']['text']}'")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_queue)
        self.timer.start(100)

    def popmesbox(self, strs):
        showMessageBox("控制中心", strs)

    def start_ssvep(self):
        self.stop()
        if self.ui.rb_ssvep.isChecked():
            print("进入 SSVEP 测试模式")
            self.pgui = Process(target=siProcess, args=(self.layout, self.ctrsetting, self.que))
        else:
            print("进入 SSVEP 小车模式")
            self.pgui = Process(target=siProcess, args=(self.layout, self.ctrsetting, self.que))
        self.pgui.start()

    def check_queue(self):
        try:
            if not self.que.empty():
                cmd = self.que.get_nowait()
                if isinstance(cmd, bytes):
                    cmd = cmd.decode("ascii")
                self.qtsig.emit(cmd)
        except:
            pass

    def stop(self):
        if self.pgui is not None:
            try:
                self.pgui.terminate()
                self.pgui.join(timeout=2)
            except:
                pass
            self.pgui = None

    def close(self):
        self.stop()
        super().close()


class stimInterface(HGuiEngine):
    def __init__(self, stim, ctr, que=None):
        super(stimInterface, self).__init__(stim)
        self.que = que
        self.ctr = ctr

        self.commadsmap = []
        for c in ctr["commands"]:
            self.commadsmap.append(wheelcmds[c])

        self.currentStep = self.startstep
        self.cmd = 0

        # 启动后立刻打印实际刺激对象的文字属性，确认引擎是否继承了这些参数
        print("引擎初始化完毕，当前刺激块文字属性：")
        for i in range(6):
            sti = self.stimuli["sti%d" % i]
            print(f"  sti{i}: text='{sti.text}'  textcolor={sti.textcolor}  start={sti.start}")

        # UDP 监听（小车模式）
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind(("127.0.0.1", 8093))
        except Exception as e:
            print(f"UDP端口绑定失败: {e}")
            self.sock.close()
            self.sock = None
        if self.sock:
            self.sock.settimeout(0.5)
            thread = threading.Thread(target=self.udp_listen, daemon=True)
            thread.start()

    def udp_listen(self):
        while True:
            try:
                buf, addr = self.sock.recvfrom(64)
                self.cmd = int(buf.decode("utf-8"))
            except socket.timeout:
                continue
            except Exception as e:
                print(f"UDP监听结束: {e}")
                break
        if self.sock:
            self.sock.close()

    def startstep(self):
        print("刺激开始前（startstep）文字颜色检查：")
        for i in range(6):
            sti = self.stimuli["sti%d" % i]
            print(f"  sti{i}: textcolor={sti.textcolor}")
        time.sleep(3)
        self.currentStep = self.flashStep

    def flashStep(self):
        with self.lock:
            for i in range(6):
                sti = self.stimuli["sti%d" % i]
                sti.start = True
                sti.bordercolor = (150, 150, 150)
                sti.textcolor = (0, 255, 0)   # 强制绿色
        time.sleep(self.ctr["flashTime"])
        self.currentStep = self.actionStep

    def actionStep(self):
        if self.que is not None:
            self.que.put(self.commadsmap[self.cmd])

        with self.lock:
            for i in range(6):
                sti = self.stimuli["sti%d" % i]
                sti.start = False
                sti.bordercolor = (150, 150, 150)
                sti.textcolor = (0, 255, 0)
            self.stimuli["sti%d" % (self.cmd)].bordercolor = (255, 0, 0)

        time.sleep(self.ctr["period"][self.cmd])
        self.currentStep = self.breakStep

    def breakStep(self):
        with self.lock:
            for i in range(6):
                sti = self.stimuli["sti%d" % i]
                sti.bordercolor = (150, 150, 150)
                sti.textcolor = (0, 255, 0)
        time.sleep(1)
        self.currentStep = self.flashStep

def siProcess(stim, ctr, que):
    si = stimInterface(stim, ctr, que)
    si.mainLoop()