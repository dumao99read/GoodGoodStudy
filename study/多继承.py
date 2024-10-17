

class Father():
    def __init__(self, name, sex='男'):
        self.name = name
        self.sex = sex

    def fangfa1(self):
        print('爸爸姓:{},性别是{}'.format(self.name, self.sex))

class Mother():
    def __init__(self, name, ability):
        self.name = name
        self.ability = ability

    def fangfa2(self):
        print('妈妈姓:{},能力是{}'.format(self.name, self.ability))

class Son(Father, Mother):
    def __init__(self, name, sex, ability, job='程序员'):
        Father.__init__(self, name, sex)
        Mother.__init__(self, name, ability)
        self.job = job

    def fangfa3(self):
        print('儿子姓:{},性别是{},能力是{},职业是{}'.format(self.name, self.sex, self.ability, self.job))

class Daughter(Mother,Father):
    def __init__(self, name, ability, sex1='女', job='测试'):
        Father.__init__(self, name)
        Mother.__init__(self, name, ability)
        self.sex1 = sex1
        self.job = job

    def fangfa3(self):
        print('女儿姓:{},性别是{},能力是{},职业是{}'.format(self.name, self.sex1, self.ability, self.job))

a = Son('刘','男','写代码')
b = Daughter('刘','鼠标点点点')
a.fangfa3()
a.fangfa2()
a.fangfa1()
b.fangfa3()
b.fangfa2()
b.fangfa1()

