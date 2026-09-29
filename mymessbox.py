from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont

def showMessageBox(title, text):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.setIcon(QMessageBox.Warning)
    
    msg_box.setFont(QFont("微软雅黑", 10))
    
    msg_box.setStyleSheet("\n        QMessageBox {\n            background-color: rgb(50, 55, 62);\n            border: 1px solid #2979ff;\n        }\n\n        QMessageBox QLabel {\n            color: white;\n            font-size: 1.2em;\n            padding: 10px;\n        }\n\n        QMessageBox QPushButton {\n            background-color: #409eff;\n            color: white;\n            border: 1px solid #2979ff;\n            border-radius: 5px;\n            padding: 10px;\n            font-size: 1.2em;\n            font-weight: bold;\n            min-width: 80px;\n        }\n\n        QMessageBox QPushButton:hover {\n            background-color: #66b1ff;\n        }\n\n        QMessageBox QPushButton:pressed {\n            background-color: #3a8ee6;\n            padding-left: 12px;\n            padding-top: 12px;\n        }\n    ")
    
    msg_box.exec_()
    return True
