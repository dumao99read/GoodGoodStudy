
person = {'sex':'男','age':'30','handsome':'Yes'}
print(person['sex'])
print(person['age'])
print(person['handsome'])
print('*******************************')

for tezheng in person.keys():
    print('key',tezheng)
    print('value',person[tezheng])
for tezheng2 in person.values():
    print('tezheng2',tezheng2)
print('########################')
for key,value in person.items():
    print(key,value)