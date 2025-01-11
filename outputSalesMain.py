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

import openpyxl
from PyQt5 import QtGui, QtWidgets
# from PyQt5 import Qt  # 从库找类大全
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
# from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.uic import loadUi

from ui.about import Ui_Form
from ui.outputSalesWin import Ui_OutputSales
from res import res


class WorkThread(QThread):
    # 信号池
    work_target = pyqtSignal(str)  # 竞猜目标值，传递给主线程

    # work_time = pyqtSignal(int)  # 时间值，用于进度条的进度展示
    def __init__(self, length, times):
        super().__init__()
        self.length = length  # 从主线程传递过来的实例参数
        self.times = times

    def run(self):
        time.sleep(1)
        num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        str_list = random.sample(num_list, self.length)
        target_number = ''.join(str_list)
        self.work_target.emit(target_number)




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
        self.pushButton_start.clicked.connect(self.start_game)  # 开始游戏
        self.action_start.triggered.connect(self.start_game)

        self.pushButton_control.clicked.connect(self.set_game)  # 游戏设置

        self.pushButton_exit.clicked.connect(self.exit_game)  # 退出游戏
        self.action_exit.triggered.connect(self.exit_game)

        self.pushButton_confirm.clicked.connect(self.confirem_and_check_result)  # 输入确认
        self.pushButton_confirm_2.clicked.connect(self.control_game)  # 设置确定
        self.action_help.triggered.connect(self.abountBtn)  # 关于按钮
        self.action_mute.triggered.connect(self.muteBtn)  # 静音按钮

    # 控制游戏参数
    def control_game(self):
        self.length = self.spinBox_length.value()  # 游戏竞猜数字长度
        self.times = self.spinBox_times.value()  # 游戏竞猜次数
        self.calculate_value = self.spinBox_times.value()  # 除数

        self.spinBox_length.setEnabled(False)
        self.spinBox_times.setEnabled(False)
        self.pushButton_confirm_2.setEnabled(False)

        # 退出游戏设置时，重新开启游戏开始的按钮
        self.lineEdit.setEnabled(False)
        self.pushButton_confirm.setEnabled(False)
        self.pushButton_start.setEnabled(True)

    def muteBtn(self):
        if self.music.volume() != 0:
            self.music.setVolume(0)
            self.action_mute.setText("取消静音")
        else:
            self.music.setVolume(5)
            self.action_mute.setText("静音")

    # 生成数字不能重复的目标数字
    def create_target_number(self, value):
        self.target_number = value
        self.progressBar.setValue(100)
        print('已接收目标值：', self.target_number)
        time.sleep(1)
        self.xtime.stop()
        self.progressBar.setValue(0)
        self.pushButton_confirm.setEnabled(True)
        self.textBrowser.setText('准备就绪。游戏开始！\n您还有{}次机会'.format(self.times))

    # 输入合理的竞猜数字
    def input_guess_number(self):
        self.guess_number = self.lineEdit.text()
        if not self.guess_number:
            print('输入为空，请重新输入！')
            QMessageBox.about(self, "警告", "输入为空，请重新输入！")
            return False
        else:
            num_list = list(self.guess_number)
            num_set = set(self.guess_number)
            if self.guess_number.isdigit() == False:
                QMessageBox.about(self, "警告", "输入的不是纯数字，无法评估。请重新输入！")
                return False
            elif len(str(self.guess_number)) != self.length:
                QMessageBox.about(self, "警告", "输入长度有误，无法评估。请重新输入！")
                return False
            elif len(num_list) != len(num_set):
                QMessageBox.about(self, "警告", "有重复数字，无法评估。请重新输入！")
                return False
            else:
                return True

    # 判断竞猜结果
    def check_result(self, target_number, input_number):
        count_a = 0
        count_b = 0
        list_target = list(target_number)
        list_input = list(input_number)
        for item in list_input:
            if item in list_target:
                if list_input.index(item) == list_target.index(item):
                    count_a += 1
                else:
                    count_b += 1
        return '{}A{}B'.format(count_a, count_b)

    def update_progress(self):
        progress = self.progressBar.value()
        if self.progressBar.value() != 99:
            self.progressBar.setValue(progress + 1)
        else:
            return

    def pushBtn(self):
        # TODO

    def calculate_progress(self):
        """适用于重复点击按钮时增长进度条"""
        self.progressBar.setMaximum(self.calculate_value)
        if self.times != 0:
            self.progressBar.setValue(self.progressBar.value() + 1)
        else:
            self.progressBar.setValue(self.calculate_value)

    def confirem_and_check_result(self):
        result = self.input_guess_number()
        if result:
            pass
        else:
            return

        self.calculate_progress()
        self.times -= 1
        info = self.check_result(self.target_number, self.guess_number)  # 判断竞猜结果
        print('输出结果：', self.target_number, self.guess_number)
        if self.times != 0 and info != '{}A0B'.format(self.length):
            self.textBrowser.append('{}的检查结果为:{},你还剩下{}次机会'.format(self.guess_number, info, self.times))
        elif self.times == 0 and info != '{}A0B'.format(self.length):
            QMessageBox.about(self, "提示", "很抱歉，你输了,正确答案是：{}".format(self.target_number))
            self.textBrowser.append('很抱歉，你输了,正确答案是：{}'.format(self.target_number))
            self.textBrowser.append('\n请点击游戏菜单退出or重新开始！' * 6)
            self.lineEdit.setEnabled(False)
            self.pushButton_confirm.setEnabled(False)
            self.pushButton_start.setEnabled(True)
        else:
            QMessageBox.about(self, "提示", "{}的检查结果为:{}。恭喜你答对了！".format(self.guess_number, info))
            self.textBrowser.append('{}的检查结果为:{}。恭喜你答对了！'.format(self.guess_number, info))
            self.textBrowser.append('\n请点击游戏菜单退出or重新开始！' * 6)
            self.lineEdit.setEnabled(False)
            self.pushButton_confirm.setEnabled(False)
            self.pushButton_start.setEnabled(True)

        self.lineEdit.clear()


if __name__ == '__main__':
    import sys

    # TODO : 使用进程后，如果打包成exe，这里需要加一行代码
    app = QtWidgets.QApplication(sys.argv)
    win = OutputSales()
    win.show()
    sys.exit(app.exec_())
