from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from .mymessbox import showMessageBox
from .rda import RDA

BAUDRATE = 460_800

class devManager(QtWidgets.QDialog):
    _sig2mesbox = pyqtSignal(str)
    def __init__(self, parentUI, queDev2Plot, setting):
        super(devManager, self).__init__()
        self.ui = parentUI
        self.RDA = RDA(self._sig2mesbox, queDev2Plot, setting)
        self.ui.startacq_btn.clicked.connect(self.start_acq)
        self.ui.stop_btn.clicked.connect(self.stop_acq)
        self.ui.device_cmb.clicked.connect(self._updatedevice)

        self._sig2mesbox.connect(self.popmesbox)

        self.datapath = "./data"
        self._updatedevice()

    def _updatedevice(self):
        device = self.RDA.getallserial()
        self.ui.device_cmb.clear()
        if len(device) > 0:
            self.ui.device_cmb.addItems(device)

    def release(self):
        self.stop_acq()

    def popmesbox(self, strs):
        showMessageBox("设备管理器", strs)

    def start_acq(self):
        # 1. 如果串口已经打开，先强制关闭（防止残留）
        if self.RDA.ser is not None:
            try:
                self.RDA.ser.close()
            except:
                pass
            self.RDA.ser = None

        # 2. 刷新设备列表
        self._updatedevice()
        if self.ui.device_cmb.count() == 0:
            showMessageBox("设备管理器", "没有找到设备！")
            return

        # 3. 获取端口并尝试打开
        portstring = self.ui.device_cmb.currentText()
        port = self.RDA.getportfromstring(portstring)
        self.RDA.configDev(port, BAUDRATE)

        if not self.RDA.startAcq():
            showMessageBox("设备管理器", "设备打开失败！")
        else:
            # 可选：提示打开成功
            pass
    def stop_acq(self):
        self.RDA.stopAcq()

    def close(self):
        self.stop_acq()