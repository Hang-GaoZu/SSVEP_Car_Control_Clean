from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from .viewerui import Ui_MainWindow  # 已改为绝对导入
from .devmanager import devManager

from .eegdisplay import EEGDisplay
from .mymessbox import showMessageBox
from queue import Queue

from .readconfig import readconfig
import sys
import traceback

class gmViewer(QtWidgets.QMainWindow):
    def __init__(self, configpath=None):
        super(gmViewer, self).__init__()
        print("[1] gmViewer 初始化开始")

        self.queDev2Plot = Queue()
        print("[2] 创建 UI")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        print("[3] UI 创建完成")

        self._screenResize()
        print("[4] 屏幕尺寸调整完成")

        print("[5] 开始读取配置文件...")
        err, setting = readconfig("./expconfig.xls")
        print(f"[6] 配置文件读取结果: err={err}")

        if err:
            print("[!] 配置文件读取失败，调用 showMessageBox 并退出")
            showMessageBox("参数读取器", "实验参数读取失败！")
            sys.exit(0)

        freqs = []
        for item in setting["layout"]:
            freqs.append(item["freq"])

        expsetting = {"freqs": freqs, "flashTime": setting["ctr"]["flashTime"]}
        print(f"[7] 实验设置: {expsetting}")

        print("[8] 创建 devManager...")
        self.devMgr = devManager(self.ui, self.queDev2Plot, expsetting)
        print("[9] devManager 创建完毕")

        print("[10] 创建 EEGDisplay...")
        self.eegDis = EEGDisplay(self.ui, self.queDev2Plot)
        print("[11] EEGDisplay 创建完毕")
        print("[12] gmViewer 初始化完成")

    def _screenResize(self):
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry(0)
        self.ww = screen_rect.width()
        self.hh = screen_rect.height()
        self.w = int((self.ww) * 0.92)
        self.h = int((self.hh) * 0.8)
        self.setGeometry(int(((self.ww) - (self.w)) / 2), int(((self.hh) - (self.h)) / 2), self.w, self.h)

    def closeEvent(self, event):
        self.devMgr.stop_acq()
        self.eegDis.close()

if __name__ == "__main__":
    print("=== EEGViewer 启动 ===")
    try:
        import multiprocessing

        multiprocessing.freeze_support()
        app = QApplication(sys.argv)
        print("QApplication 创建成功")

        a = gmViewer()
        print("gmViewer 实例创建成功，准备显示窗口...")
        a.show()
        print("窗口已调用 show()")

        sys.exit(app.exec_())
    except Exception:
        traceback.print_exc()
        print("程序异常退出")
    finally:
        print("=== 程序结束 ===")