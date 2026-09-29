from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from wheeltec import WheelTec
from mymessbox import showMessageBox

BAUDRATE = 9600

class WheelManager(QtWidgets.QDialog):
    _sig2mesbox = pyqtSignal(str)

    def __init__(self, parentUI, qtsig):
        super(WheelManager, self).__init__()
        self.ui = parentUI
        self.wheel = WheelTec()
        self.deviceOpened = False

        # 初始禁用相关按钮
        self.ui.bt_back.setEnabled(False)
        self.ui.bt_fwr.setEnabled(False)
        self.ui.bt_lturn.setEnabled(False)
        self.ui.bt_rturn.setEnabled(False)
        self.ui.bt_sound.setEnabled(False)
        self.ui.bt_flash.setEnabled(False)
        self.ui.bt_startssvepvehicle.setEnabled(False)
        self.ui.bt_startssvep.setEnabled(False)
        self.ui.bt_close.setEnabled(False)

        # 连接信号
        qtsig.connect(self.vmove)
        self.ui.deviceCBox.clicked.connect(self._updatedevice)
        self.ui.bt_open.clicked.connect(self.vopen)
        self.ui.bt_close.clicked.connect(self.vclose)
        self.ui.bt_back.clicked.connect(self.cback)
        self.ui.bt_fwr.clicked.connect(self.cfwr)
        self.ui.bt_lturn.clicked.connect(self.clturn)
        self.ui.bt_rturn.clicked.connect(self.crturn)
        self.ui.bt_sound.clicked.connect(self.csound)
        self.ui.bt_flash.clicked.connect(self.cflash)

        self.ui.rb_manual.setChecked(True)
        self.ui.rb_manual.toggled.connect(self.updateRb)
        self.ui.rb_ssvep.toggled.connect(self.updateRb)
        self.ui.rb_ssvepvehicle.toggled.connect(self.updateRb)
        self._updatedevice()

    def close(self):
        self.wheel.close()

    def updateRb(self):
        if self.ui.rb_manual.isChecked():
            self.ui.bt_startssvep.setEnabled(False)
            self.ui.bt_startssvepvehicle.setEnabled(False)
            if self.deviceOpened:
                self.ui.bt_back.setEnabled(True)
                self.ui.bt_fwr.setEnabled(True)
                self.ui.bt_lturn.setEnabled(True)
                self.ui.bt_rturn.setEnabled(True)
                self.ui.bt_sound.setEnabled(True)
                self.ui.bt_flash.setEnabled(True)
            else:
                self.ui.bt_back.setEnabled(False)
                self.ui.bt_fwr.setEnabled(False)
                self.ui.bt_lturn.setEnabled(False)
                self.ui.bt_rturn.setEnabled(False)
                self.ui.bt_sound.setEnabled(False)
                self.ui.bt_flash.setEnabled(False)
        elif self.ui.rb_ssvep.isChecked():
            self.ui.bt_startssvep.setEnabled(True)
            self.ui.bt_startssvepvehicle.setEnabled(False)
            self.ui.bt_back.setEnabled(False)
            self.ui.bt_fwr.setEnabled(False)
            self.ui.bt_lturn.setEnabled(False)
            self.ui.bt_rturn.setEnabled(False)
            self.ui.bt_sound.setEnabled(False)
            self.ui.bt_flash.setEnabled(False)
        elif self.ui.rb_ssvepvehicle.isChecked():
            self.ui.bt_startssvep.setEnabled(False)
            if self.deviceOpened:
                self.ui.bt_startssvepvehicle.setEnabled(True)
            else:
                self.ui.bt_startssvepvehicle.setEnabled(False)
            self.ui.bt_back.setEnabled(False)
            self.ui.bt_fwr.setEnabled(False)
            self.ui.bt_lturn.setEnabled(False)
            self.ui.bt_rturn.setEnabled(False)
            self.ui.bt_sound.setEnabled(False)
            self.ui.bt_flash.setEnabled(False)

    def vopen(self):
        if self.checkdeviceport():
            self.deviceOpened = True
            self.updateRb()
            self.ui.bt_close.setEnabled(True)
            self.ui.bt_open.setEnabled(False)
        else:
            self.deviceOpened = False
            self.updateRb()
            self.ui.bt_close.setEnabled(False)
            self.ui.bt_open.setEnabled(True)

    def vclose(self):
        self.wheel.close()
        self.deviceOpened = False
        self.ui.bt_back.setEnabled(False)
        self.ui.bt_fwr.setEnabled(False)
        self.ui.bt_lturn.setEnabled(False)
        self.ui.bt_rturn.setEnabled(False)
        self.ui.bt_sound.setEnabled(False)
        self.ui.bt_flash.setEnabled(False)
        self.ui.bt_startssvepvehicle.setEnabled(False)
        self.ui.bt_open.setEnabled(True)
        self.ui.bt_close.setEnabled(False)

    def vmove(self, cmd_str):
        print("\n[WheelManager.vmove] ========== 收到命令 ==========")
        print(f"  命令内容: {cmd_str}")
        print(f"  命令类型: {type(cmd_str)}")
        print(f"  串口状态: deviceOpened={self.deviceOpened}")
        print(f"  串口对象: {self.wheel.ser}")
        
        if self.wheel.ser is not None:
            print(f"  串口是否打开: {self.wheel.ser.is_open}")
            print(f"  串口端口: {self.wheel.ser.port}")
        else:
            print("  警告: 串口对象为 None!")
        
        if self.deviceOpened:
            print("  正在发送命令到串口...")
            try:
                self.wheel.sendCmd(cmd_str)
                print("  命令发送完成")
            except Exception as e:
                print(f"  发送失败: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("  ❌ 错误: 串口未打开，命令未发送！")
            print("  提示: 请先点击'打开'按钮连接小车")
        
        print("[WheelManager.vmove] ==================================\n")

    # 按钮动作（已加保护，防止未打开时崩溃）
    def cback(self):
        if self.deviceOpened:
            self.wheel.sendCmd("1")
        else:
            print("串口未打开，无法发送后退指令")

    def cfwr(self):
        if self.deviceOpened:
            self.wheel.sendCmd("2")
        else:
            print("串口未打开，无法发送前进指令")

    def clturn(self):
        if self.deviceOpened:
            self.wheel.sendCmd("3")
        else:
            print("串口未打开，无法发送左转指令")

    def crturn(self):
        if self.deviceOpened:
            self.wheel.sendCmd("4")
        else:
            print("串口未打开，无法发送右转指令")

    def csound(self):
        if self.deviceOpened:
            self.wheel.sendCmd("6")
        else:
            print("串口未打开，无法发送鸣笛指令")

    def cflash(self):
        if self.deviceOpened:
            self.wheel.sendCmd("5")
        else:
            print("串口未打开，无法发送亮灯指令")

    def _updatedevice(self):
        device = self.wheel.getallserial()
        self.ui.deviceCBox.clear()
        if len(device) > 0:
            self.ui.deviceCBox.addItems(device)

    def popmesbox(self, strs):
        showMessageBox("控制中心", strs)

    def checkdeviceport(self):
        # 修复逻辑错误：initSer成功返回True，失败返回False
        if self.ui.deviceCBox.count() == 0:
            self._updatedevice()
            if self.ui.deviceCBox.count() == 0:
                showMessageBox("控制中心", "没有搜索到端口，请先连接小车蓝牙！")
                return False
        port = self.ui.deviceCBox.currentText()
        # initSer 返回 True 表示成功，此时不要弹错误框
        if not self.wheel.initSer(port):
            showMessageBox("控制中心", "小车端口打开失败！可能被占用！")
            return False
        return True