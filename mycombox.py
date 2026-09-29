"""
Time    : 2025/5/28 12:04
Author  : mrtang
Email   : 810899799@qq.com
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

class MyComboBox(QtWidgets.QComboBox):
    clicked = pyqtSignal()
    def showPopup(self):
        self.clicked.emit()
        super(MyComboBox, self).showPopup()
