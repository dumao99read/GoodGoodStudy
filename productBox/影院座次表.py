a = 11  # 外循环的排数
b = 11  # 内循环的座次数
c = 10  # 排列无法对齐的界点(十位，百位..百位暂不考虑)

for i in range(1, a+1):
    for j in range(1, b+1):
        if i < c and j < c:
            print("0{}排0{}座".format(i, j), end=' ')
        elif i < c and j >= c:
            print("0{}排{}座".format(i, j), end=' ')
        elif i >= c and j < 10:
            print("{}排0{}座".format(i, j), end=' ')
        else:
            print("{}排{}座".format(i, j), end=' ')
    print(' ')
