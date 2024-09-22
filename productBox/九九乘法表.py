a=1 #乘法表的起始被乘数
b=12 #乘法表的终点乘数

for i in range(a,b+1):
    #print("第{}行：".format(i,i+1))
    for j in range(a,i+1):
        #print(j,'*',i,'=',i*j,end=" ")
            if j*i<10:
                print(str(j) + '*' + str(i) + '=' + str(i * j), end="   ") #循环里面不换行，就使用end函数
            elif j*i<100:
                print(str(j) + '*' + str(i) + '=' + str(i * j), end="  ") #循环里面不换行，就使用end函数
            else:
                print(str(j) + '*' + str(i) + '=' + str(i * j), end=" ") #循环里面不换行，就使用end函数
    print("") #代表换行