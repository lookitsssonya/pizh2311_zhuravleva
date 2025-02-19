class Person:
    def __init__(self, n, s, q=1):
        self.name = n
        self.surname = s
        self.skill = q
    def __del__(self):
        print("До свидания, мистер", self.name, self.surname)
    def info(self):
        return "{} {}, {}".format(self.name, self.surname, self.skill)

worker = Person("И", "Котов", 3)
helper = Person("Д", "Мышев", 1)
maker = Person("O", "Рисов", 2)
print(worker.info())
print(helper.info())
print(maker.info())
del helper
print("Конец программы")
input()