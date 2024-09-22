"""
===========================
Author:独毛
Time:2023/6/23_21:10
Project:PycharmProjects
Remark:
===========================
"""
import random

gameControl = 'Y'
jj = 0
while int(jj) < 3 and (gameControl == 'Y' or gameControl == 'y'):
    X = 3
    # X = input("请输入你想竞猜的次数X=：")
    print("""
    肖娟宝宝，生日快到了。
    加华哥哥为肖娟宝宝准备了10个生日礼物盲盒竞猜，其中只有一个为真正要送出的礼物。
    生日礼物盲盒如下：
    1)项链； 2）发卡； 3）100块钱； 4）蛋糕； 5）衣服；
    6）包包； 7）手机； 8）4个鸡蛋； 9）再送一条乐乐； 10）报个瑜伽班；
    11)大明星的瓜； 12）送花； 13）把乐乐毒打一顿； 14）送护肤套装； 15）游乐场一天游；
    16)浪漫表白； 17）请吃饭； 18）送个小孩； 19）送你回娘家； 20）溜冰滑雪。
    游戏开始，你只有{}次竞猜机会。请输入你要猜的盲盒序号（从1到10）""".format(X))
    list_gift = {"1":"项链","2":"发卡","3":"100块钱","4":"蛋糕","5":"衣服","6":"包包","7":"手机","8":"4个鸡蛋","9":"再送一条乐乐","10":"报个瑜伽班",
                 "11":"大明星的瓜","12":"送花","13":"把乐乐毒打一顿","14":"送护肤套装","15":"游乐场一天游","16":"浪漫表白","17":"请吃饭",
                 "18":"送个小孩","19":"送你回娘家","20":"溜冰滑雪"}
    randomNumber = random.randint(1, 20)
    gift = list_gift.get(str(randomNumber))
    #print(randomNumber,gift)
    i = 0
    while i in range(0, int(X)):
        guessNumber = input('请输入你猜想的礼物序号,数字在1到20之间：')
        c = guessNumber.isdigit() and len(guessNumber) <= 2
        if c == True and int(guessNumber)<=20:
            i += 1
            if int(guessNumber) == randomNumber:
                print('Happy Birthday to XiaoJuan！\n您的生日礼物【{}】将在你生日当天送出,请注意查收！'.format(gift))
                break
            elif int(i) ==  int(X):
                print('非常抱歉，您的生日礼物【{}】无法送出，请明年生日继续竞猜！'.format(gift))
                break
            elif int(guessNumber) > randomNumber:
                print('竞猜错误，生日礼物的序号【靠前】！你还剩{}次机会。'.format(int(X)-i))
                continue
            else:
                print('竞猜错误，生日礼物的序号【靠后】！你还剩{}次机会。'.format(int(X)-i))
                continue
        else:
            print('输入有误，请输入你猜想的礼物序号,数字在1到20之间')
    jj += 1
    if int(jj) <3:
        gameControl = input("是否重新开始游戏？输入Y并回车会重新开始游戏，输入其他内容并回车退出游戏：")
input("游戏结束，再见！")