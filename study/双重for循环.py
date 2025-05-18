a=1
b=9

for i in range(a,b):
    #print("第{}行：".format(index,index+1))
    for j in range(a,i+1):
        print(j,end=" ") #循环里面不换行，就使用end函数
    print("") #代表换行