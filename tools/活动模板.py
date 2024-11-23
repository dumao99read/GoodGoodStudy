import os.path


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.uic import loadUi

CURR_PATH = os.path.dirname(__file__)
DEBUG = True


class $LEINAME$(QtWidgets.QMainWindow, Ui_GuessNumber):

    def __init__(self):
        super().__init__()

        # 初始化ui界面，DEBUG为True时不需要转换文件，适合调界面样式；为False时需要转换文件，适合调新增控件
        if DEBUG:
            # 直接加载ui文件，好处是不需要转换成py文件直接取用最新设置，坏处是新增控件无法直接联想
            # 此时虽然继承了guessNumberWindow.py的Ui_GuessNumber类，但是不会使用py文件里面的旧内容
            ui_path = os.path.join(CURR_PATH, "$UI$.ui")
            loadUi(ui_path, self)
        else:
            self.setupUi(self)


        # 建立信号槽连接
        self.initUI()

    def initUI(self):
        # 信号槽链接
        $XINHAO$

     $FUNCTION$




if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = $LEINAME$()
    win.show()
    sys.exit(app.exec_())