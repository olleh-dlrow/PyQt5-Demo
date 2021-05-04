# Ui文件生成的py文件
from demo_music import Ui_MainWindow
from PyQt5.Qt import *
import sys

# 主窗口
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(1200, 800)

if __name__ == '__main__':
    # 初始化APP
    app = QApplication(sys.argv)
    # 创建窗口
    win = MainWindow()
    # 绘制窗口
    win.show()
    # 循环绘制
    sys.exit(app.exec_())