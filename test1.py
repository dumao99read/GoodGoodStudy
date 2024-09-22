

x = {"a":"1","b":2}
y = {"a":"1","b":"2"}
print(type(x))
print(list(x.values()))

print(type(y))
print(list(y.keys()))

z = []

for item in x.items():
    print(item,type(item))

print(666)