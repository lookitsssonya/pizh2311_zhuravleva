from random import randint

class Soldier:
    health = 100
    def set_name(self, name):
        self.name = name

    def make_kick(self, enemy):
        enemy.health -= 20
        print(self.name, "бьет", enemy.name)
        print('%s = %d' % (enemy.name, enemy.health))

class Battle:
    result = "Сражения не было"

    def battle(self, u1, u2):
        while u1.health > 0 and u2.health > 0:
            n = randint(1, 2)
            if n == 1:
                u1.make_kick(u2)
            else:
                u2.make_kick(u1)
        if u1.health > u2.health:
            self.result = u1.name + " ПОБЕДИЛ"
        elif u2.health > u1.health:
            self.result = u2.name + " ПОБЕДИЛ"

    def who_win(self):
        print(self.result)

first = Soldier()
second = Soldier()
first.set_name('A')
second.set_name('B')

b = Battle()
b.battle(first, second)
b.who_win()