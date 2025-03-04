# Лабораторная работа на неделю 2
## **Дисциплина**: Объектно-ориентированное программирование
### Выполнила студентка группы ПИЖ-б-о-23-1(1) Журавлева Софья Витальевна 
**Репозиторий Git:** https://github.com/lookitsssonya/pizh2311_zhuravleva <br></br>
**Вариант: 9**  <br></br>
**Практическая работа:** <br></br>
Класс «ПчёлоСлон»  
Экземпляр класса инициализируется двумя целыми числами: первое относится к пчеле, второе - к слону. 
Класс реализует следующие методы: 
1) fly() - может летать - возвращает True, если часть пчелы не меньше части слона, иначе False; 
2) trumpet() - трубить - если часть слона не меньше части пчелы, возвращает строку: "tu-tu-doo-doo!", иначе "wzzzzz". 
3) eat(meal, value) - есть - может есть только нектар (nectar) или траву (grass). Если съедает нектар, то из части слона вычитается количество съеденного, пчеле добавляется, иначе наоборот: у пчелы вычитается, а слону добавляется. Не может увеличиться выше 100 и уменьшиться меньше 0; 
4) get_parts() - возвращает список значений: [часть пчелы, часть слона]. 

*Ответ:*  
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    """
    Абстрактный базовый класс для представления животных.
    """
    def __init__(self, part: int):
        """
        Инициализация животного.

        :param part: Часть животного (целое число от 0 до 100).
        """
        self.part = part

    @abstractmethod
    def make_sound(self) -> str:
        """
        Абстрактный метод для издания звука животным.

        :return: Строка, представляющая звук животного.
        """
        pass

    def get_part(self) -> int:
        """
        Возвращает текущее значение части животного.

        :return: Целое число, представляющее часть животного.
        """
        return self.part


class Bee(Animal):
    """
    Класс, представляющий пчелу.
    """
    def make_sound(self) -> str:
        """
        Возвращает звук, издаваемый пчелой.

        :return: Строка "wzzzzz".
        """
        return "wzzzzz"


class Elephant(Animal):
    """
    Класс, представляющий слона.
    """
    def make_sound(self) -> str:
        """
        Возвращает звук, издаваемый слоном.

        :return: Строка "tu-tu-doo-doo!".
        """
        return "tu-tu-doo-doo!"


class BeeElephant:
    """
    Класс, представляющий гибрид пчелы и слона.
    """
    def __init__(self, bee_part: int, elephant_part: int):
        """
        Инициализация гибрида пчелы и слона.

        :param bee_part: Часть пчелы (целое число от 0 до 100).
        :param elephant_part: Часть слона (целое число от 0 до 100).
        """
        self.bee = Bee(bee_part)
        self.elephant = Elephant(elephant_part)

    def fly(self) -> bool:
        """
        Определяет, может ли гибрид летать.

        :return: True, если часть пчелы не меньше части слона, иначе False.
        """
        return self.bee.get_part() >= self.elephant.get_part()

    def trumpet(self) -> str:
        """
        Определяет, какой звук издает гибрид.

        :return: "tu-tu-doo-doo!", если часть слона не меньше части пчелы, иначе "wzzzzz".
        """
        if self.elephant.get_part() >= self.bee.get_part():
            return self.elephant.make_sound()
        else:
            return self.bee.make_sound()

    def eat(self, meal: str, value: int) -> None:
        """
        Позволяет гибриду есть нектар или траву.

        :param meal: Тип еды ("nectar" или "grass").
        :param value: Количество съеденного (целое число).
        """
        if meal == "nectar":
            self.elephant.part = max(0, min(100, self.elephant.part - value))
            self.bee.part = max(0, min(100, self.bee.part + value))
        elif meal == "grass":
            self.bee.part = max(0, min(100, self.bee.part - value))
            self.elephant.part = max(0, min(100, self.elephant.part + value))

    def get_parts(self) -> list[int]:
        """
        Возвращает текущие значения частей пчелы и слона.

        :return: Список из двух целых чисел: [часть пчелы, часть слона].
        """
        return [self.bee.get_part(), self.elephant.get_part()]

    def __call__(self) -> str:
        """
        Возвращает строковое представление текущего состояния гибрида.

        :return: Строка в формате "Bee part: X, Elephant part: Y".
        """
        return f"Bee part: {self.bee.get_part()}, Elephant part: {self.elephant.get_part()}"

    def __eq__(self, other: 'BeeElephant') -> bool:
        """
        Сравнивает два объекта BeeElephant по их частям.

        :param other: Другой объект BeeElephant.
        :return: True, если части пчелы и слона равны, иначе False.
        """
        return (self.bee.get_part() == other.bee.get_part() and
                self.elephant.get_part() == other.elephant.get_part())


# Пример использования
bee_elephant1 = BeeElephant(60, 40)
bee_elephant2 = BeeElephant(60, 40)
bee_elephant3 = BeeElephant(50, 50)

# Проверка метода fly()
print(bee_elephant1.fly())  # Результат: True, так как часть пчелы (60) >= часть слона (40)

# Проверка метода trumpet()
print(bee_elephant1.trumpet())  # Результат: "wzzzzz", так как часть пчелы (60) > часть слона (40)

# Проверка метода eat()
bee_elephant1.eat("nectar", 20)
print(bee_elephant1.get_parts())  # Результат: [80, 20], так как часть пчелы увеличилась на 20, а часть слона уменьшилась на 20

bee_elephant1.eat("grass", 10)
print(bee_elephant1.get_parts())  # Результат: [70, 30], так как часть пчелы уменьшилась на 10, а часть слона увеличилась на 10

# Проверка вызываемого метода
print(bee_elephant1())  # Результат: Bee part: 70, Elephant part: 30

# Проверка перегрузки __eq__
print(bee_elephant1 == bee_elephant2)  # Результат: False, так как части разные
print(bee_elephant2 == bee_elephant3)  # Результат: False, так как части разные
print(bee_elephant2 == BeeElephant(60, 40))  # Результат: True, так как части одинаковые
```  
Вывод программы:  
True   
wzzzzz  
[80, 20]  
[70, 30]  
Bee part: 70, Elephant part: 30  
False  
False  
True   

**UML** <br>
<img src="./uml/uml.png">