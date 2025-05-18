"""
===========================
Author:独毛
Time:2023/6/23_13:38
Project:PycharmProjects
Remark:
===========================
"""
import random
def randomNumber():
    global i
    global j
    global k
    global l
    i = random.randint(0,9)
    j = random.randint(0,9)
    while i == j:
        j = random.randint(0,9)
    k = random.randint(0,9)
    while k == j or k == i:
        k = random.randint(0,9)
    l = random.randint(0,9)
    while l == k or l == j or l == i:
        l = random.randint(0,9)
    return (i,j,k,l)


gameControl = 'Y'
while gameControl == 'Y' or gameControl == 'y':
    print("""
    游戏规则说明：
    1）从0~9中选取4个不重复的数字，视为猜数字，一共有X次竞猜机会（X由玩家控制）；
    2）每猜一次，系统会返回当前猜数字的结果，用A和B来代替：
        ①如果有一个数字和位置都猜对了，记作1A，如果有一个数字猜对了但位置错了，记作1B，
          A的优先级比B高（意思就是已经记作A的数字，不会再统计B）
        ②当4个数字和位置都正确时，记作4A0B，玩家胜利；当4个数字都正确但位置都错误时，记作0A4B；
          如果所有数字都没有猜对，记作0A0B。
        ③请充分利用数字不能重复和系统返回的猜数字结果，猜想你心中的答案吧。祝你好运！""")

    X = input("请输入你想竞猜的次数X=：")
    a = randomNumber()
    #print("系统给出的随机数是：",a)
    c = str(a[0])+str(a[1])+str(a[2])+str(a[3]) #重组a，方便打印给玩家知晓正确答案
    ii = 0
    while ii in range(0, int(X)):
        b = input("请输入0-9的4个不重复数字：")
        if b.isdigit() == False:
            print("输入的不是纯数字，无法评估。请重新输入！")
            continue
        elif len(str(b)) != 4:
            print("输入长度有误，无法评估。请重新输入！")
            continue
        m = b[0]
        n = b[1]
        o = b[2]
        p = b[3]
        countA = 0
        countB = 0
        #从这里开始，多个if判断数字和位置都正确，取值countA加1
        if int(m) == int(i):
            countA += 1
        if int(n) == int(j):
            countA +=1
        if int(o) == int(k):
            countA +=1
        if int(p) == int(l):
            countA +=1
        #从这里开始，多个if判断数字正确但位置不正确，取值countB加1
        if int(m) == int(j) or int(m) == int(k) or int(m) == int(l):
            countB += 1
        if int(n) == int(i) or int(n) == int(k) or int(n) == int(l):
            countB += 1
        if int(o) == int(i) or int(o) == int(j) or int(o) == int(l):
            countB += 1
        if int(p) == int(i) or int(p) == int(j) or int(p) == int(k):
            countB += 1
        #从这里开始，多个if判断输入结果
        if countA == 4 and countB == 0:
            print("评估结果为：{}A{}B,恭喜你猜对了！".format(countA,countB))
            break
        if int(m) == int(n) or int(m) == int(o) or int(m) == int(p):
            print("输入了重复数字，无法评估。请重新输入！")
            continue
        if int(n) == int(o) or int(n) == int(p):
            print("输入了重复数字，无法评估。请重新输入！")
            continue
        if int(o) == int(p):
            print("输入了重复数字，无法评估。请重新输入！")
            continue
        else:
            ii += 1
        if ii == int(X):
            print("没猜对，竞猜结束，当前是第{}轮竞猜，评估竞猜结果为：{}A{}B。正确答案是：".format(ii,countA,countB),c)
            break
        else:
            print("没猜对，请继续下一轮。当前是第{}轮竞猜。评估猜测结果为：{}A{}B".format(ii,countA,countB))
    gameControl = input("是否重新开始游戏？输入Y并回车会重新开始游戏，输入其他内容并回车退出游戏：")
input("是否退出游戏？:")