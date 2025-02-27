class Pizza:
    """Класс Pizza содержит общие атрибуты для пиццы."""

    def __init__(self):
        """Конструктор класса."""
        self.name = "Заготовка"
        self.dough = "тонкое"
        self.sauce = "кетчуп"
        self.filling = []
        self.price = 0

    def __str__(self) -> str:
        """Вернуть информацию о пицце."""
        return (f"Пицца: {self.name} | Цена: {self.price:.2f} р.\n"
                f"Тесто: {self.dough} Соус: {self.sauce}\n"
                f"Начинка: {', '.join(self.filling)}")

    def prepare(self) -> None:
        """Сообщить о процессе подготовки."""
        print(f"Начинаю готовить пиццу {self.name}")
        print(f"  - замешиваю {self.dough} тесто...")
        print(f"  - добавляю соус: {self.sauce}...")
        print(f"  - и, конечно: {', '.join(self.filling)}...")

    def bake(self) -> None:
        """Сообщить о процессе запекания."""
        print("Выпекаю пиццу... Готово!")

    def slice(self) -> None:
        """Сообщить о процессе нарезки."""
        print("Нарезаю на аппетитные кусочки...")

    def pack(self) -> None:
        """Сообщить о процессе упаковки."""
        print("Упаковываю в фирменную упаковку и готово!")


class Peperoni(Pizza):
    """Класс Peperoni дополняет класс Pizza."""

    def __init__(self):
        super().__init__()
        self.name = "Пепперони"
        self.sauce = "томатный"
        self.filling = ["пепперони", "сыр моцарелла"]
        self.price = 350.00


class Barbecue(Pizza):
    """Класс Barbecue дополняет класс Pizza."""

    def __init__(self):
        super().__init__()
        self.name = "Барбекю"
        self.sauce = "барбекю"
        self.filling = ["бекон", "ветчина", "зелень", "сыр моцарелла"]
        self.price = 450.00


class Seafood(Pizza):
    """Класс Seafood дополняет класс Pizza."""

    def __init__(self):
        super().__init__()
        self.name = "Дары моря"
        self.dough = "пышное"
        self.sauce = "тар-тар"
        self.filling = ["кальмары", "креветки", "мидии", "сыр моцарелла"]
        self.price = 550.00
