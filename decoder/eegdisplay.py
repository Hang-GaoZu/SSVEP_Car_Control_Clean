import pyqtgraph as pg
pg.setConfigOption("background", (50, 55, 62))
from .datamanager import DataManager
from .butterfilter import ButterFilter
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from .commonsetting import *

COLORS = [(255, 0, 0), (0, 0, 255), (0, 0, 0), (255, 0, 255)]
yscale = [20, 50, 100, 200, 500, 2, 10, 100, 1, 5, 0]
ygain = [1, 1, 1, 1, 1, 0.001, 0.001, 0.001, 0.000001, 0.000001, 1]

class EEGDisplay(QWidget):
    _psig = pyqtSignal(str)

    def __init__(self, parentUI, que):
        super(EEGDisplay, self).__init__()
        self.que = que
        self.batC = 80
        self.batUC = 0
        self.flttype = 2
        self.ygain = 1
        self.curves = []
        self.batlevel = 8
        self.period = 0
        self.relayouting = False

        # ------ 数据管理器 ------
        self.dm = DataManager()
        self.chsNum = 8  # 硬件真实通道数
        # 只显示 CH1~CH6（索引 2~7），隐藏 GND(0) 和 REF(1)
        self.visible_channels = [2, 3, 4, 5, 6, 7]
        self.dataSrate = 250
        self.localSrate = 250
        self.dm.config(self.localSrate, self.chsNum, XPERIOD, EEGTYPE)

        self.ui = parentUI
        self.ui.yrange_cmb.currentIndexChanged.connect(lambda: self.relayout(rtype=0))

        # ------ 绘图区域 ------
        self.pgplot = pg.PlotWidget()
        self.pgplot.showGrid(True, True)

        # ------ 滤波器 ------
        self.filter = ButterFilter()
        self.filter.reset(srate=250, chs=self.chsNum,
                          fltparam=[(49, 51), (1, 45), (1, 0)],
                          eegtype=EEGTYPE)

        self.ui.displayLayout.addWidget(self.pgplot)
        self.pgplot.show()
        self.pgTimer = pg.QtCore.QTimer()
        self.pgTimer.timeout.connect(self.update_one_frame)
        self.pgTimer.start(5)

        # 初始创建可见通道数量的曲线
        self.relayout(rtype=1)

    def close(self):
        self.pgTimer.stop()
        self.pgTimer.deleteLater()

    def relayout(self, rtype=0):
        self.relayouting = True
        scale = yscale[self.ui.yrange_cmb.currentIndex()]
        self.ygain = ygain[self.ui.yrange_cmb.currentIndex()]
        visible_count = len(self.visible_channels)

        if rtype == 1:
            self.pgplot.clear()
            self.curves = []
            self.pgplot.setYRange(0, scale * visible_count)
            self.pgplot.setXRange(0, self.localSrate * XPERIOD)
            for visual_idx, ch_idx in enumerate(self.visible_channels):
                curve = pg.PlotCurveItem(pen=pg.mkPen(color=(50, 255, 50), width=1))
                self.pgplot.addItem(curve)
                curve.setPos(0, visual_idx * scale + 0.5 * scale)
                self.curves.append(curve)
        else:
            if len(self.curves) == 0:
                self.relayouting = False
                return
            self.pgplot.setYRange(0, scale * visible_count)
            for visual_idx in range(visible_count):
                self.curves[visual_idx].setPos(0, visual_idx * scale + 0.5 * scale)

        self.relayouting = False

    def update_one_frame(self):
        if self.relayouting:
            return

        while not self.que.empty():
            dat = self.que.get()
            self.batlevel = dat.get("batlevel", 8)
            self.dataSrate = dat.get("srate", 250)
            dataay = dat["dataay"]
            chs, N = dataay.shape
            if chs != self.chsNum:
                self.chsNum = chs
                self.relayout(rtype=1)
                return

            eeg = dataay[:, :]
            self.filter.update(eeg)

            if self.flttype == 0:
                self.dm.update(self.filter.rawdata)
            elif self.flttype == 1:
                self.dm.update(self.filter.hdata)
            elif self.flttype == 2:
                self.dm.update(self.filter.bdata)
            else:
                self.dm.update(self.filter.rawdata)

        if self.dm.data is None:
            return

        # 只绘制可见通道的数据
        for visual_idx, ch_idx in enumerate(self.visible_channels):
            if visual_idx < len(self.curves) and ch_idx < self.dm.data.shape[0]:
                self.curves[visual_idx].setData(self.dm.data[ch_idx, :] * self.ygain)

        self.batUC += 1
        self.batUC %= self.batC
        if self.batUC == 0:
            self.ui.batLevel.setValue(int(self.batlevel * 10))