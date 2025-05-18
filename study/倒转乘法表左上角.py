a=9 #外循环的被乘数
b=9 #内循环的乘数

for i in range(1,a+1):
    for j in range(i,b+1):
        print(str(i)+'*'+str(j)+'='+str(i*j),end=" ")#循环里面不换行，就使用end函数
    print(" ") #代表换行