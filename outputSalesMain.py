# -*-coding:utf-8-*-
"""
===========================
Author:独毛
Time:2024/3/24_13:40
Project:PycharmProjects
Remark:
===========================
"""
import os.path
import os.path
import random
import time
import logging

import openpyxl
from PyQt5 import QtGui, QtWidgets
# from PyQt5 import Qt  # 从库找类大全
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
# from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

from ui.about import Ui_Form
from ui.outputSalesWin import Ui_OutputSales
from res import res

logging.basicConfig(level=logging.INFO,
                    encoding='UTF-8',
                    filename='导出销售日志.log',
                    filemode='a',
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class WorkThread(QThread):
    # 信号池
    work_done = pyqtSignal(str)  # 任务完成的信号

    # work_time = pyqtSignal(int)  # 时间值，用于进度条的进度展示
    def __init__(self, length, times):
        super().__init__()
        self.length = length  # 从主线程传递过来的实例参数
        self.times = times

    def run(self):
        self.work_done.emit()


class About(QtWidgets.QMainWindow, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class OutputSales(QtWidgets.QMainWindow, Ui_OutputSales):

    def __init__(self, target_number='', guess_number=''):
        super().__init__()
        self.current_dir = os.getcwd()
        self.new_workbook_name = ''

        # 初始化ui界面
        self.setupUi(self)

        # 初始化音乐
        self.initMusic()

        # 建立信号槽连接
        self.initUI()

    def abountBtn(self):
        self.about = About()
        self.about.setWindowTitle("关于")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/png/img/lele.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.about.setWindowIcon(icon)

        self.about.show()

    def initMusic(self):
        self.music = QMediaPlayer()  # 播放器
        self.music.setVolume(5)  # 设置音量
        # url = QUrl("qrc:/mp3/music/piliyouxia.mp3")
        # list_player = self.music.setMedia(QMediaContent(url))
        # self.music.playlist()

        url = QUrl("qrc:/group1/music/doudizhu.wav")
        self.play_list = QMediaPlaylist()  # 播放列表
        self.play_list.addMedia(QMediaContent(url))
        self.music.setPlaylist(self.play_list)  # 设置播放清单
        self.play_list.setPlaybackMode(QMediaPlaylist.Loop)  # 循环播放
        self.music.play()

    def open_file(self):
        if self.new_workbook_name != '' and self.new_workbook_name is not None:
            file_path = self.new_workbook_name  # 先点击按钮1，则按钮2直接判断了按钮1生成的文件并直接获取
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", self.current_dir, "Excel files(*.xlsx)")

        # 检查用户是否选择了文件
        if file_path:
            QMessageBox.information(self, "文件路径", f"你选择的文件路径是：{file_path}")
            # 使用 os.path.basename 提取文件名，对单个文件有效
            filename = os.path.basename(file_path)
            print(filename)
            return file_path, openpyxl.load_workbook(file_path)

        else:
            QMessageBox.information(self, "info-提示", "文件未选择")
            return None, None

    def initUI(self):
        # 信号槽链接
        self.pushButton_start.clicked.connect(self.start_output)  # 开始输出

        self.action_help.triggered.connect(self.abountBtn)  # 关于按钮
        self.action_mute.triggered.connect(self.muteBtn)  # 静音按钮

    def muteBtn(self):
        if self.music.volume() != 0:
            self.music.setVolume(0)
            self.action_mute.setText("取消静音")
        else:
            self.music.setVolume(5)
            self.action_mute.setText("静音")

    def update_progress(self):
        progress = self.progressBar.value()
        if self.progressBar.value() != 99:
            self.progressBar.setValue(progress + 1)
        else:
            return

    def start_output(self):
        logging.info('开始导出任务！')
        self.pushButton_start.setEnabled(False)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)

        self.xtime = QTimer()
        self.xtime.timeout.connect(self.update_progress)
        self.xtime.start(100)  # 每隔多少毫秒调度一次定时器，用于进度条渐进



if __name__ == '__main__':
    import sys

    # TODO : 使用进程后，如果打包成exe，这里需要加一行代码
    app = QtWidgets.QApplication(sys.argv)
    win = OutputSales()
    win.show()
    sys.exit(app.exec_())
