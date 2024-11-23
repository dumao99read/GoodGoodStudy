import os.path
import random


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.uic import loadUi
from fighter import Ui_MainWindow

CURR_PATH = os.path.dirname(__file__)


class ShiTouJianDaoBu(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.fighter_list = ["加","减","平"]


        # 建立信号槽连接
        self.initUI()

    def initUI(self):
        # 信号槽链接
        self.pushButton.clicked.connect(self.clickBtn)

    def create_fighter(self):
        # 从样本里随机取数，取一个少一个，依次取3个
        round_1 = random.sample(self.fighter_list, 3)
        round_2 = random.sample(self.fighter_list, 3)
        result = self.fighter(round_1, round_2)
        if result:
            return round_1, round_2
        else:
            return self.create_fighter()  # False的时候，重新执行本方法，直到结果为True

    def fighter(self, round_1, round_2):
        """
        对比两个列表中的元素，如果有任意位置元素相同，就返回False：
        如果所有位置元素都不相同，就返回True
        """
        for i,j in zip(round_1,round_2):
            if i == j:  # 如果有两个值相同，则返回False
                return False
            else:
                pass
        else:  # 如果for遍历没有中断(即3次对比没有相同值)，就返回True
            return True

    def clickBtn(self):
        self.textBrowser.clear()
        self.textBrowser_2.clear()

        x, y = self.create_fighter()

        self.textBrowser.append("玩家1")
        self.textBrowser.append("石头：" + x[0])
        self.textBrowser.append("剪刀：" + x[1])
        self.textBrowser.append("布：" + x[2])

        self.textBrowser_2.append("玩家2")
        self.textBrowser_2.append("石头：" + y[0])
        self.textBrowser_2.append("剪刀：" + y[1])
        self.textBrowser_2.append("布：" + y[2])


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = ShiTouJianDaoBu()
    win.show()
    sys.exit(app.exec_())