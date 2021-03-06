from demo_music import Ui_MainWindow
from find import *
from like import *
from collect import *

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedLayout, QWidget, QStatusBar, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QCursor
import sys
import time
import _thread

class FindPage(QWidget, Ui_find):
    def clicked(self):
        print(self.pushButton.text() + ' clicked')

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.clicked)
        self.pushButton.pressed.connect(lambda :print(self.pushButton.text() + ' pressed'))
        self.pushButton.released.connect(lambda :print(self.pushButton.text() + ' released'))

        self.checkBox.stateChanged.connect(lambda :print(self.checkBox.text() + ' stateChanged'))
        self.checkBox_2.stateChanged.connect(lambda :print(self.checkBox_2.text() + ' is checked') if self.checkBox_2.isChecked() else None)

        self.radioButton.toggled.connect(lambda :print(self.radioButton.text() + ' toggled'))
        self.radioButton_2.toggled.connect(lambda :print(self.radioButton_2.text() + ' toggled'))

class LikePage(QWidget, Ui_like):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(lambda :print(self.label.text() + ' ' + self.lineEdit.text() +
                                                      '\n' + self.label_2.text() + ' ' + self.lineEdit_2.text()))

        self.pushButton_2.clicked.connect(lambda : print(self.comboBox.currentText()))
        # if currentText == ?: do something

class CollectPage(QWidget, Ui_collect):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.putInCenter()
        # self.setFixedSize(1445, 837)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint)
        # self.setWindowOpacity(0.9)  # ?????????????????????
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # ????????????????????????

        # ?????????
        self.qsl = QStackedLayout(self.parts)

        self.find = FindPage()
        self.like = LikePage()
        self.collect = CollectPage()

        self.qsl.addWidget(self.find)
        self.qsl.addWidget(self.like)
        self.qsl.addWidget(self.collect)

        self.controller()

        # ????????????
        self.m_flag = False
        self.m_Position = 0

        # ????????????
        self.playing = False
        self.tid = 0

        # status bar
        self.statusbar = QStatusBar()
        self.bottomLayout.addWidget(self.statusbar)

    # ??????????????????????????????????????????
    def putInCenter(self):
        # ?????????????????????
        screen = QDesktopWidget().screenGeometry()
        # ?????????????????????
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft),int(newTop))

    def controller(self):
        # ??????????????????
        self.closePushButton.clicked.connect(self.close)
        self.minPushButton.clicked.connect(self.showMinimized)

        # ????????????
        self.backButton.clicked.connect(self.onBackEvent)
        self.forwardButton.clicked.connect(self.onForwardEvent)
        self.playingButton.clicked.connect(self.onPlayEvent)


        # ???????????????
        self.findPushButton.clicked.connect(self.switch)
        self.likePushButton.clicked.connect(self.switch)
        self.collectPushButton.clicked.connect(self.switch)
        pass

    def onBackEvent(self):
        self.progressBar.setValue(0)
        self.playing = False
        self.changePlayButtonImage()
        pass

    def onForwardEvent(self):
        self.progressBar.setValue(0)
        self.playing = False
        self.changePlayButtonImage()
        pass

    def onPlayEvent(self):
        if self.playing:
            self.playing = False
            self.changePlayButtonImage()
        else:
            self.playing = True
            self.changePlayButtonImage()
            _thread.start_new_thread(self.increaseProgressBar, ())

            # self.increaseProgressBar()
        pass

    def increaseProgressBar(self):
        while self.playing and self.progressBar.value() < self.progressBar.maximum():
            if self.progressBar.value() + 5 <= self.progressBar.maximum():
                self.progressBar.setValue(self.progressBar.value() + 5)
            else:
                self.progressBar.setValue(self.progressBar.maximum())
            time.sleep(1)


        if self.playing and self.progressBar.value() == self.progressBar.maximum():
            self.progressBar.setValue(0)
            self.playing = False
            self.changePlayButtonImage()

    def changePlayButtonImage(self):
        if not self.playing:
            self.playingButton.setStyleSheet('.QPushButton{\n'
'background-image: url(:/center-stop/center-stop.jpg);\n'
'border: 1px solid #D8D8D8;\n'
'}\n'
'.QPushButton:hover{\n'
'background-image: url(:/center-stop/center-stop-hover.jpg);\n'
'}')
        else:
            self.playingButton.setStyleSheet('.QPushButton{'
'background-image: url(:/center/center.jpg);'
'border: 1px solid #D8D8D8;'
'}'
'.QPushButton:hover{'
'background-image: url(:/center/center-hover.jpg);'
'}')

    def switch(self):
        sender = self.sender().objectName()
        index = {
            "findPushButton": 0,
            "likePushButton": 1,
            "collectPushButton": 2
        }
        self.qsl.setCurrentIndex(index[sender])
        # self.like.lineEdit_2.setFocus()
        pass

    def add_shadow(self):
        # ????????????
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0,0) # ??????
        self.effect_shadow.setBlurRadius(10) # ????????????
        self.effect_shadow.setColor(QtCore.Qt.gray) # ????????????
        self.setGraphicsEffect(self.effect_shadow) # ??????????????????widget?????????

    #????????????
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.top.geometry().contains(self.mapFromGlobal(QCursor.pos())):
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            # self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag and self.top.geometry().contains(self.mapFromGlobal(QCursor.pos())):
            self.move(event.globalPos() - self.m_Position)
            event.accept()


    def mouseReleaseEvent(self, event):
        if Qt.LeftButton and self.top.geometry().contains(self.mapFromGlobal(QCursor.pos())):
            self.m_flag = False
        # self.setCursor(QCursor(Qt.ArrowCursor))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    pass
