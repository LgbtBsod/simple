import time
import sys
import os
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QWidget, QLabel, QLayout, QPushButton
from PyQt6.QtCore import Qt
from clientui import Ui_IM
import requests
from datetime import datetime



class example(QtWidgets.QDialog, Ui_IM):
    leftClick = False

    def __init__(self, url):
        super().__init__()
        self.mess = ''

        self.setupUi(self)
        self.url = url
        self.old_pos = None
        self.pushButton.pressed.connect(self.send_message)
        self.after = time.time() - 24 * 60 * 60

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_message)
        self.timer.start(1000)

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        #self.center()

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


    def add_text(self, text):

        self.textBrowser.append(text)
        self.textBrowser.append('\n')

    def login(self, nick, password):

        self.nick = nick
        self.password = password

    @staticmethod
    def format_message(m):
        name = m['name']
        text = m['text']
        dt = datetime.fromtimestamp(m['time'])
        dt_beauty = dt.strftime("%A, %d. %B %Y %I:%M%p")
        return f'{name} {dt_beauty}\n {text}'

    def update_message(self):
        try:
            response = requests.get(f'{self.url}messages', params={'after': self.after})
        except:
            return
        messages = response.json()['messages']
        for m in messages:
            self.add_text(self.format_message(m))
            self.after = m['time']

    def send_message(self):
        #name = self.name.text()
        #password = self.password.text()
        text = self.textEdit.toPlainText()
        if not self.nick or not self.password or not text:
            self.add_text('Please enter data')
            return False

        message = {'name': self.nick,
                   'text': text,
                   'password': self.password}
        try:
            response = requests.post(f'{self.url}send', json=message)
        except:
            self.add_text('Server Offline')
            return False

        if response.status_code == 200:
            self.textEdit.setText('')
            self.textEdit.repaint()
        elif response.status_code == 401:
            self.add_text('Error, invalid name or password')
        else:
            self.add_text('Error, try later')


#if __name__ == "__main__":
#def start():
    #app = QtWidgets.QApplication(sys.argv)
    #window = example('http://127.0.0.1:5000/')
    #window.show()
    #sys.exit(app.exec())

