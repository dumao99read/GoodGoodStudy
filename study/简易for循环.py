list = ['张三','李四','王五','赵六']

for index in list:
    print("name",index)
for name in range(len(list)):
    print("index",list[name])

person = {'sex':'男','age':'30','handsome':'Yes'}
for key in person:
    print('key',key)
    print(person[key])

print(person.values())
print('@@@@@@@@@@@@@')
for value1 in person:
    print(value1)
    print('value',person[value1])