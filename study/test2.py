def a():
    print(1)
def b(x):
    x = a
    x()

#x = a()
b(a)