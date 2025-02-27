import time

class Order:
    """Класс Order содержит информацию о заказе."""

    order_counter = 0

    def __init__(self):
        """Конструктор класса."""
        self.ordered_pizzas = []
        Order.order_counter += 1
        self.order_number = Order.order_counter

    def __str__(self) -> str:
        """Вернуть содержимое заказа и его сумму."""
        res = f"Заказ №{self.order_number}\n"
        for i, pizza in enumerate(self.ordered_pizzas, 1):
            res += f"{i}. {pizza}\n"
        res += f"Сумма заказа: {self.amount():.2f} р.\n"
        return res

    def add(self, pizza) -> None:
        """Добавить пиццу в заказ."""
        self.ordered_pizzas.append(pizza)
        print(f"Пицца {pizza.name} добавлена!")

    def amount(self) -> float:
        """Вернуть сумму заказа."""
        return sum(pizza.price for pizza in self.ordered_pizzas)

    def complete(self) -> None:
        """Выполнить заказ."""
        print(f"Заказ поступил на выполнение...")
        for i, pizza in enumerate(self.ordered_pizzas, 1):
            print(f"{i}. {pizza.name}")
            pizza.prepare()
            pizza.bake()
            pizza.slice()
            pizza.pack()
            time.sleep(1)
        print(f"Заказ №{self.order_number} готов! Приятного аппетита!")
