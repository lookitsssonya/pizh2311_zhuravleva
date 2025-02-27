from order import Order
from pizza import Peperoni, Barbecue, Seafood

class Terminal:
    """Класс Terminal обеспечивает взаимодействие с клиентом."""

    COMPANY = "Пиццерия #1"
    COMMAND_CANCELL_ORDER = -1
    COMMAND_CONFIRM_ORDER = 0

    def __init__(self):
        """Конструктор класса."""
        self.menu = [Peperoni(), Barbecue(), Seafood()]
        self.order = None
        self.display_menu = True

    def __str__(self) -> str:
        """Вернуть строковое представление класса."""
        return f"{self.COMPANY}, версия программы 1.0"

    def show_menu(self) -> None:
        """Показать меню."""
        if not self.display_menu:
            return

        print(f"{self.COMPANY}\nДобро пожаловать!\n")
        print("Меню:")
        for i, pizza in enumerate(self.menu, 1):
            print(f"{i}. {pizza}")
        print("Для выбора укажите цифру через <ENTER>.")
        print("Для отмены заказа введите -1")
        print("Для подтверждения заказа введите 0")
        self.display_menu = False

    def process_command(self, menu_item: str) -> None:
        """Обработать действие пользователя."""
        try:
            menu_item = int(menu_item)
            if menu_item == self.COMMAND_CANCELL_ORDER:
                if self.order:
                    print("Заказ отменен.")
                    self.order = None
                else:
                    print("Нет активного заказа для отмены.")
            elif menu_item == self.COMMAND_CONFIRM_ORDER:
                if self.order:
                    print("Заказ подтвержден.")
                    print(self.order)
                    self.accept_payment()
                    self.order.complete()
                    self.order = None
                else:
                    print("Нет активного заказа для подтверждения.")
            elif 1 <= menu_item <= len(self.menu):
                if not self.order:
                    self.order = Order()
                self.order.add(self.menu[menu_item - 1])
            else:
                raise ValueError
        except ValueError:
            print("Не могу распознать команду! Проверьте ввод.")
        except Exception as e:
            print(f"Во время работы терминала произошла ошибка: {e}")

    def calculate_change(self, payment: float) -> float:
        """Вернуть сдачу для 'оплата'."""
        if payment < self.order.amount():
            raise ValueError("Оплата меньше суммы заказа.")
        return payment - self.order.amount()

    def accept_payment(self) -> None:
        """Обработать оплату."""
        try:
            payment = float(input("Введите сумму: "))
            change = self.calculate_change(payment)
            print(f"Вы внесли {payment:.2f} р. Сдача: {change:.2f} р.")
        except Exception as e:
            print(f"Оплата не удалась: {e}")
            raise
