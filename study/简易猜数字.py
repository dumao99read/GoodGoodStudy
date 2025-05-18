"""
===========================
Author:独毛
Time:2023/6/23_13:38
Project:PycharmProjects
Remark:
===========================
"""
import random
gameControl = 'Y'

while gameControl == 'Y' or gameControl == 'y':
    print("""
    游戏规则说明：
    1）系统随机给出一个1到1000的数字，玩家有X次竞猜次数(X由玩家控制)；
    2）每次玩家竞猜后，系统根据结果提示玩家的竞猜值太【大】或者太【小】；
    请根据系统提示开始竞猜吧。祝你好运！""")
    randomNumber = random.randint(0, 1000)
    X = input("请输入你想竞猜的次数X=：")
    #print(randomNumber)
    i = 0
    while i in range(0, int(X)):
        guessNumber = input('请输入你猜想的数字,数字在1到1000之间：')
        c = guessNumber.isdigit() and len(guessNumber) < 5
        if c == True and int(guessNumber)<=1000:
            i += 1
            if int(guessNumber) == randomNumber:
                print('恭喜你猜对了！！！当前已猜{0}次!'.format(i))
                break
            elif int(i) ==  int(X):
                print('竞猜次数已达上限{0}次，竞猜数字为{1}。'.format(i, randomNumber))
                break
            elif int(guessNumber) > randomNumber:
                print('你猜想的数字太【大】了！请重新猜。当前已猜{0}次：'.format(i))
                continue
            else:
                print('你猜想的数字太【小】了！请重新猜。当前已猜{0}次：'.format(i))
                continue
        else:
            print('输入有误，请重新输入你猜想的数字!')
    gameControl = input("是否重新开始游戏？输入Y并回车会重新开始游戏，输入其他内容并回车退出游戏：")