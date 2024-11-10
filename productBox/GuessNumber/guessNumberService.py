# -*-coding:utf-8-*-
"""
===========================
Author:独毛
Time:2024/3/24_13:40
Project:PycharmProjects
Remark:
===========================
"""

import random
import time

class GuessNumber:

    cls_length = 4
    cls_times = 8

    def __init__(self, target_number='', guess_number=''):
        self.target_numer = target_number # 目标值
        self.guess_number = guess_number  # 竞猜值
        # 将类属性赋值给实例属性，好处是更新类属性值后，下一个实例的初始属性跟着变化，达到设置游戏参数的效果。
        self.length = GuessNumber.cls_length  # 竞猜的数字长度
        self.times = GuessNumber.cls_times  # 竞猜次数

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
                ③请充分利用数字不能重复和系统返回的猜数字结果，猜想你心中的答案吧。祝你好运！""".format(self.length,self.times))
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
        GuessNumber.cls_length = int(input('请输入竞猜数字长度(3~5之间)：'))
        GuessNumber.cls_times = int(input('请输入竞猜次数（1~10之间）：'))
        # self.length = GuessNumber.cls_length
        # self.times = GuessNumber.cls_times
        # self.show_game_menu()
        # 重启实例
        game = GuessNumber()
        game.show_game_menu()


    # 生成数字不能重复的目标数字
    def create_target_number(self):
        num_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        str_list = random.sample(num_list, self.length)
        self.target_number = ''.join(str_list)
        print(self.target_number)
        return self.target_number

    # 输入合理的竞猜数字
    def input_guess_number(self):
        check = True
        while check == True:
            self.guess_number = input("请输入0-9的{}个不重复数字：".format(self.length))
            num_list = list(self.guess_number)
            num_set = set(self.guess_number)
            if self.guess_number.isdigit() == False:
                print("输入的不是纯数字，无法评估。请重新输入！")
                continue
            elif len(str(self.guess_number)) != self.length:
                print("输入长度有误，无法评估。请重新输入！")
                continue
            elif len(num_list) != len(num_set):
                print("有重复数字，无法评估。请重新输入！")
                continue
            else:
                check = False
                return self.guess_number

    # 判断竞猜结果
    def check_result(self,target_number,input_number):
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
        return '{}A{}B'.format(count_a,count_b)

    def run(self):
        res = self.create_target_number()
        info = ''
        while self.times != 0 and info != '{}A0B'.format(self.length):
            info = self.check_result(res, self.input_guess_number())
            self.times -= 1
            print('此次竞猜结果为:{},你还剩下{}次机会'.format(info,self.times))
        if self.times == 0 and info != '{}A0B'.format(self.length):
            print('很抱歉，你输了,正确答案是：{}'.format(self.target_number))
        else:
            print('恭喜你答对了！')
        time.sleep(1.5)
        game = GuessNumber()
        game.show_game_menu()

if __name__ == '__main__':
    game = GuessNumber()
    game.show_game_menu()



