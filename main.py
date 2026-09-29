"""
Time    : 2025/5/28 12:11
Author  : mrtang
Email   : 810899799@qq.com
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal
import sys
import multiprocessing
from wheelmanager import WheelManager
from readconfig import readconfig
from controlcenterUI import Ui_MainWindow
from stimulimanager import StiManager
from mymessbox import showMessageBox
import subprocess
#解决乱码

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
process_name = "controlCenter.exe"

def killall(name=process_name):
    try:
        subprocess.run(["taskkill", "/f", "/im", name], check=True)
        print(f"已终止所有 {name} 进程")
    except subprocess.CalledProcessError:
        print(f"未找到 {name} 进程，或无法终止")
    except Exception as e:
        print(f"发生错误: {e}")

class contrlCenter(QtWidgets.QMainWindow):
    sigctr = pyqtSignal(str)

    def __init__(self):
        print("初始化主窗口...")
        super(contrlCenter, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        print("UI 加载完毕")

        print("正在读取配置文件...")
        err, setting = readconfig("./expconfig.xls")
        if err:
            print("配置文件读取失败，程序即将退出")
            showMessageBox("控制中心", "实验参数读取失败！")
            sys.exit(0)
        print("配置文件读取成功")
        print(setting)
        print("初始化 WheelManager...")
        self.wMgr = WheelManager(self.ui, self.sigctr)
        print("初始化 StiManager...")
        self.stiMgr = StiManager(self.ui, setting, self.sigctr)
        print("主窗口初始化完成")

    def closeEvent(self, e):
        print("关闭事件触发")
        self.wMgr.close()
        self.stiMgr.close()
        killall()

if __name__ == "__main__":
    print("程序开始运行")
    multiprocessing.freeze_support()

    # 如果之前的实例还在，先杀掉
    killall()

    app = QApplication(sys.argv)
    print("QApplication 创建完成")

    a = contrlCenter()
    a.show()
    print("主窗口已显示")

    print("进入事件循环...")
    exit_code = app.exec_()
    print(f"事件循环结束，退出码: {exit_code}")
    sys.exit(exit_code)