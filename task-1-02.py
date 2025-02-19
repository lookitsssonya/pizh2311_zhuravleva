from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def eat(self, meal, value):
        pass

    @abstractmethod
    def get_parts(self):
        pass

class BeeElephant(Animal):
    def __init__(self, bee_part, elephant_part):
        if 0 <= bee_part <= 100 and 0 <= elephant_part <= 100:
            self.__bee_part = bee_part
            self.__elephant_part = elephant_part
        else:
            raise ValueError("Части должны быть в пределах от 0 до 100.")

    def fly(self):
        return self.__bee_part >= self.__elephant_part

    def trumpet(self):
        if self.__elephant_part >= self.__bee_part:
            return "tu-tu-doo-doo!"
        else:
            return "wzzzzz"

    def eat(self, meal, value):
        if meal == "nectar":
            if self.__elephant_part - value >= 0 and self.__bee_part + value <= 100:
                self.__elephant_part -= value
                self.__bee_part += value
            else:
                raise ValueError("Значение выходит за пределы.")
        elif meal == "grass":
            if self.__bee_part - value >= 0 and self.__elephant_part + value <= 100:
                self.__bee_part -= value
                self.__elephant_part += value
            else:
                raise ValueError("Значение выходит за пределы.")
        else:
            raise ValueError("Используйте 'nectar' или 'grass'.")

    def get_parts(self):
        return [self.__bee_part, self.__elephant_part]

    def __call__(self):
        return self.get_parts()


if __name__ == "__main__":
    bee_elephant = BeeElephant(50, 60)
    print(bee_elephant.get_parts())

    print(bee_elephant.fly())
    print(bee_elephant.trumpet())

    bee_elephant.eat("nectar", 10)
    print(bee_elephant.get_parts())

    bee_elephant.eat("grass", 20)
    print(bee_elephant.get_parts())

    print(bee_elephant())