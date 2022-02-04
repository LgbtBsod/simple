import sys

from PyQt6 import QtWidgets, QtCore, QtGui

from log import Ui_log
from IM import example


class log(QtWidgets.QDialog, Ui_log):
    leftClick = False

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.pushButton.pressed.connect(self.login)

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        

        self.pushButton_5.clicked.connect(lambda: self.showMinimized())
        self.pushButton_3.clicked.connect(lambda: self.close())

    def mouseMoveEvent(self, e: QtGui.QMouseEvent):
        if self._tracking:
            self._endPos = e.globalPosition().toPoint() - self._startPos
            self.move(self._winPos + self._endPos)

    def mousePressEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            self._winPos = self.pos()
            self._startPos = QtCore.QPoint(e.globalPosition().toPoint())
            self._tracking = True

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
        if e.button() == QtCore.Qt.MouseButton.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

    def login(self):
        phone = self.phone.text()
        password = self.password.text()
        nick = self.nick.text()
        if not phone or not password or not nick:
            self.add_text('Please enter data')
            pass
        else:
            self.close()
            try:
                window = example('http://127.0.0.1:5000/')
                window.login(nick, password)
                window.show()
                sys.exit(app.exec())
            except:
                pass

    def add_text(self, text):
        self.textBrowser.append(text)



app = QtWidgets.QApplication(sys.argv)
window1 = log()
window1.show()
sys.exit(app.exec())
