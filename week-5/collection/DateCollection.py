import json
from date import Date

class DateCollection:
    """Класс-контейнер для хранения и управления набором объектов Date.

    Поля:
      - _data (list[Date]): список объектов Date.

    Методы:
      - __init__(): инициализирует контейнер;
      - __str__(): возвращает строковое представление контейнера;
      - __getitem__(): позволяет индексировать и срезать контейнер;
      - add(): добавляет объект Date в контейнер;
      - remove(): удаляет объект Date из контейнера по индексу;
      - save(): сохраняет контейнер в JSON-файл;
      - load(): загружает контейнер из JSON-файла.
    """

    def __init__(self):
        """Инициализирует контейнер с пустым списком объектов Date."""
        self._data = []  
        
    def __str__(self):
        """Возвращает строковое представление контейнера в виде списка дат."""
        return "[" + ", ".join(str(date) for date in self._data) + "]"  

    def __getitem__(self, index):
        """Позволяет индексировать и срезать контейнер.

        Аргументы:
          - index (int или slice): индекс или срез для доступа к элементам.

        Возвращает:
          - Date или list[Date]: объект Date или список объектов Date.
        """
        return self._data[index]  
        
    def add(self, value: Date):
        """Добавляет объект Date в контейнер.

        Аргументы:
          - value (Date): объект Date для добавления.
        """
        self._data.append(value)  

    def remove(self, index: int):
        """Удаляет объект Date из контейнера по индексу.

        Аргументы:
          - index (int): индекс элемента для удаления.
        """
        del self._data[index]  

    def save(self, filename: str):
        """Сохраняет контейнер в JSON-файл.

        Аргументы:
          - filename (str): имя файла для сохранения.
        """
        with open(filename, 'w') as file:
            json.dump([date.to_dict() for date in self._data], file)

    def load(self, filename: str):
        """Загружает контейнер из JSON-файла.

        Аргументы:
          - filename (str): имя файла для загрузки.
        """
        with open(filename, 'r') as file:
            data = json.load(file)
            self._data = [Date.from_string(f"{d['day']}.{d['month']}.{d['year']}") for d in data]
