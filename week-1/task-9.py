from math import pi

class Cylinder:
    @staticmethod
    def make_area(d, h):
        circle = pi * d ** 2 / 4
        side = pi * d * h
        return round(circle * 2 + side, 2)

    def __init__(self, diameter, high):
        self.__dict__['dia'] = diameter
        self.__dict__['h'] = high
        self.__dict__['area'] = self.make_area(diameter, high)

    def __setattr__(self, key, value):
        if key == 'dia':
            self.__dict__['dia'] = value
            self.__dict__['area'] = self.make_area(
                self.__dict__['dia'], self.__dict__['h'])
        elif key == 'h':
            self.__dict__['h'] = value
            self.__dict__['area'] = self.make_area(
                self.__dict__['dia'], self.__dict__['h'])
        elif key == 'area':
            print('Нельзя изменять площадь напрямую!')

a = Cylinder(1, 2)
print(a.dia, a.h, a.area)

a.dia = 4.5
a.h = 3.3
print(a.dia, a.h, a.area)

# Не позволено
a.area = 100
print(a.area)