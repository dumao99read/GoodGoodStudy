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
import random
import time
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

CURR_PATH = os.path.dirname(__file__)

class GuessNumber(QtWidgets.QMainWindow):

    def __init__(self, target_number='', guess_number=''):
        super().__init__()
        # self.setupUi(self)
        # 直接加载ui文件，不需要转换成py
        ui_path = os.path.join(CURR_PATH, "guessNumberWindow.ui")
        loadUi(ui_path, self)
        self.initUI()

        self.target_numer = target_number  # 目标值
        self.guess_number = guess_number  # 竞猜值
        self.length = self.spinBox_length.value()  # 游戏竞猜数字长度
        self.times = self.spinBox_times.value()  # 游戏竞猜次数

    def initUI(self):
        # 信号槽链接
        self.pushButton_start.clicked.connect(self.start_game)  # 开始游戏
        self.action_start.triggered.connect(self.start_game)
        self.pushButton_control.clicked.connect(self.set_game)  # 游戏设置

        # self.pushButton_control.setEnabled(False)
        self.pushButton_exit.clicked.connect(self.exit_game)  # 退出游戏
        self.action_exit.triggered.connect(self.exit_game)


        self.pushButton_confirm.clicked.connect(self.confirem_and_check_result)  # 输入确认
        self.pushButton_confirm_2.clicked.connect(self.control_game)  # 设置确定

    # 展示游戏菜单
    def show_game_menu(self):
        print("""
            游戏规则说明：
            1）从0~9中选取{0}个不重复的数字，视为猜数字，一共有{1}次竞猜机会（{1}由玩家控制）；
            2）每猜一次，系统会返回当前猜数字的结果，用A和B来代替：
                ①如果有一个数字和位置都猜对了，记作1A，如果有一个数字猜对了但位置错了，记作1B，
                  A的优先级比B高（意思就是已经记作A的数字，不会再统计B）
                ②当所有数字和位置都正确时，记作{0}A0B，玩家胜利；当所有数字都正确但位置都错误时，记作0A{0}B；
                  如果所有数字都没有猜对，记作0A0B。
                ③请充分利用数字不能重复和系统返回的猜数字结果，猜想你心中的答案吧。祝你好运！""".format(self.length,
                                                                                                     self.times))
        print("""
            1，开始游戏
            2，游戏设置
            3，退出游戏
        """)
        game_mode = input("请选择：")
        if game_mode == '1':
            self.run()
        elif game_mode == '2':
            self.control_game()
        elif game_mode == '3':
            pass
        else:
            print('输入有误，请重新输入：')
            self.show_game_menu()

    # 控制游戏参数
    def control_game(self):
        self.length = self.spinBox_length.value()  # 游戏竞猜数字长度
        self.times = self.spinBox_times.value()  # 游戏竞猜次数

        self.spinBox_length.setEnabled(False)
        self.spinBox_times.setEnabled(False)
        self.pushButton_confirm_2.setEnabled(False)

        # 退出游戏设置时，重新开启游戏开始的按钮
        self.lineEdit.setEnabled(False)
        self.pushButton_confirm.setEnabled(False)
        self.pushButton_start.setEnabled(True)



    # 生成数字不能重复的目标数字
    def create_target_number(self):
        num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        str_list = random.sample(num_list, self.length)
        self.target_number = ''.join(str_list)
        print(self.target_number)
        return self.target_number

    # 输入合理的竞猜数字
    def input_guess_number(self):
            self.guess_number = self.lineEdit.text()
            if not self.guess_number:
                print('输入为空，请重新输入！')
                self.lineEdit.setText('输入为空，请重新输入！')
            else:
                num_list = list(self.guess_number)
                num_set = set(self.guess_number)
                if self.guess_number.isdigit() == False:
                    self.lineEdit.setText('输入的不是纯数字，无法评估。请重新输入！')
                elif len(str(self.guess_number)) != self.length:
                    self.lineEdit.setText('输入长度有误，无法评估。请重新输入！')
                elif len(num_list) != len(num_set):
                    self.lineEdit.setText('有重复数字，无法评估。请重新输入！')
                else:
                    return self.guess_number

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

    def start_game(self):
        self.pushButton_start.setEnabled(False)
        self.pushButton_confirm.setEnabled(True)
        self.lineEdit.clear()
        self.lineEdit.setEnabled(True)
        self.textBrowser.clear()
        self.textBrowser.setEnabled(True)

        self.times = self.spinBox_times.value()
        self.create_target_number()  # 创建目标随机数
        self.lineEdit.setPlaceholderText('')
        self.textBrowser.setText('游戏开始！您还有{}次机会'.format(self.times))

    def set_game(self):
        self.pushButton_start.setEnabled(False)
        self.lineEdit.clear()
        self.lineEdit.setEnabled(False)
        self.textBrowser.clear()
        self.textBrowser.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.textBrowser.setEnabled(False)

        self.pushButton_confirm_2.setEnabled(True)
        self.spinBox_length.setEnabled(True)
        self.spinBox_times.setEnabled(True)

    def exit_game(self):
        sys.exit()

    def confirem_and_check_result(self):
        self.input_guess_number()
        self.times -= 1
        info = self.check_result(self.target_number, self.guess_number)  # 判断竞猜结果
        if self.times != 0 and info != '{}A0B'.format(self.length):
            self.textBrowser.append('{}的检查结果为:{},你还剩下{}次机会'.format(self.guess_number, info, self.times))
        elif self.times == 0 and info != '{}A0B'.format(self.length):
            self.textBrowser.append('很抱歉，你输了,正确答案是：{}'.format(self.target_number))
            self.textBrowser.append('\n请点击游戏菜单退出or重新开始！' * 3)
            self.lineEdit.setEnabled(False)
            self.pushButton_confirm.setEnabled(False)
            self.pushButton_start.setEnabled(True)
        else:
            self.textBrowser.append('{}的检查结果为:{}。恭喜你答对了！'.format(self.guess_number, info))
            self.textBrowser.append('\n请点击游戏菜单退出or重新开始！' * 3)
            self.lineEdit.setEnabled(False)
            self.pushButton_confirm.setEnabled(False)
            self.pushButton_start.setEnabled(True)

        self.lineEdit.clear()



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = GuessNumber()
    win.show()
    sys.exit(app.exec_())
