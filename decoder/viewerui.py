from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

class MyComboBox(QtWidgets.QComboBox):
    clicked = pyqtSignal()
    def showPopup(self):
        self.clicked.emit()
        super(MyComboBox, self).showPopup()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 999)
        MainWindow.setStyleSheet("background-color: rgb(40, 44, 52);")
        
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)
        
        self.topMenuBar = QtWidgets.QFrame(self.centralwidget)
        self.topMenuBar.setStyleSheet("background-color: rgb(58, 64, 73); border-radius: 10px;")
        self.topMenuBar.setObjectName("topMenuBar")
        self.topMenuLayout = QtWidgets.QHBoxLayout(self.topMenuBar)
        self.topMenuLayout.setContentsMargins(10, 10, 10, 10)
        self.topMenuLayout.setSpacing(10)
        
        self.device_cmb = MyComboBox(self.topMenuBar)
        
        self.device_cmb.setFixedSize(200, 30)
        
        self.device_cmb.setStyleSheet("background-color: rgb(50, 55, 62); color: white; border-radius: 5px; font-size: 1.2em;")
        
        self.topMenuLayout.addWidget(self.device_cmb)
        
        self.startacq_btn = QtWidgets.QPushButton("开始采集", self.topMenuBar)
        self.startacq_btn.setFixedSize(100, 30)
        self.startacq_btn.setStyleSheet("\n        QPushButton {\n            background-color: #409eff;\n            color: white;\n            border-radius: 8px;\n            font-size: 1.6em;\n\n        }\n        QPushButton:hover {\n            background-color: #66b1ff;\n        }\n        QPushButton:pressed {\n            background-color: #3a8ee6;\n        }\n        ")
        
        self.topMenuLayout.addWidget(self.startacq_btn)
        
        self.stop_btn = QtWidgets.QPushButton("停止", self.topMenuBar)
        self.stop_btn.setFixedSize(100, 30)
        self.stop_btn.setStyleSheet("\n                QPushButton {\n                    background-color: #b10303; \n                    color: white; \n                    border-radius: 8px;\n                    font-size: 1.2em;\n\n                }\n                QPushButton:hover {\n                    background-color: #ff7875;\n                }\n                QPushButton:pressed {\n                    background-color: #d9363e;\n                }\n                ")
        
        self.topMenuLayout.addWidget(self.stop_btn)
        
        self.label_yrange = QtWidgets.QLabel("Y轴：", self.topMenuBar)
        self.label_yrange.setFixedSize(60, 30)
        self.label_yrange.setStyleSheet("color: white; font-size: 1.2em;")
        self.topMenuLayout.addWidget(self.label_yrange)
        
        self.yrange_cmb = QtWidgets.QComboBox(self.topMenuBar)
        self.yrange_cmb.setFixedSize(100, 30)
        
        self.yrange_cmb.setStyleSheet("background-color: rgb(50, 55, 62); color: white; border-radius: 5px; font-size: 1.2em;")
        
        self.yrange_cmb.addItem("20uV")
        self.yrange_cmb.addItem("50uV")
        self.yrange_cmb.addItem("100uV")
        self.yrange_cmb.addItem("200uV")
        self.yrange_cmb.addItem("500uV")
        self.yrange_cmb.addItem("2mV")
        self.yrange_cmb.addItem("10mV")
        self.yrange_cmb.addItem("100mV")
        self.yrange_cmb.addItem("1V")
        self.yrange_cmb.addItem("5V")
        self.yrange_cmb.addItem("Auto")
        self.yrange_cmb.setCurrentIndex(3)
        self.topMenuLayout.addWidget(self.yrange_cmb)
        
        self.label_battery = QtWidgets.QLabel("设备电量", self.topMenuBar)
        self.label_battery.setFixedSize(70, 30)
        self.label_battery.setStyleSheet("color: white; font-size: 1.2em;")
        self.topMenuLayout.addWidget(self.label_battery)
        
        self.batLevel = QtWidgets.QProgressBar(self.topMenuBar)
        self.batLevel.setFixedWidth(100)
        self.batLevel.setFixedHeight(25)
        self.batLevel.setAlignment(QtCore.Qt.AlignCenter)
        
        self.batLevel.setStyleSheet("background-color: rgb(50, 55, 62); color: white; border-radius: 5px; font-size: 1em;")
        
        self.batLevel.setMinimum(0)
        self.batLevel.setMaximum(100)
        self.batLevel.setValue(100)
        self.topMenuLayout.addWidget(self.batLevel)
        
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.topMenuLayout.addItem(spacer)
        
        self.mainLayout.addWidget(self.topMenuBar)
        
        self.displayArea = QtWidgets.QFrame(self.centralwidget)
        self.displayArea.setStyleSheet("background-color: rgb(50, 55, 62); border-radius: 10px;")
        self.displayArea.setObjectName("displayArea")
        self.displayLayout = QtWidgets.QVBoxLayout(self.displayArea)
        self.displayLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.addWidget(self.displayArea, stretch=1)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
