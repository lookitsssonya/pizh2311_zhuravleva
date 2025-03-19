class MoneyTransfer:
    """
    Базовый класс для денежных переводов.
    
    Атрибуты:
        amount (float): Сумма перевода.
        sender (str): Имя отправителя.
        recipient (str): Имя получателя.
        _status (str): Статус перевода (защищенное поле).
    """
    
    def __init__(self, amount, sender, recipient):
        """
        Инициализация базового класса MoneyTransfer.
        
        Аргументы:
            amount (float): Сумма перевода.
            sender (str): Имя отправителя.
            recipient (str): Имя получателя.
        """
        self.amount = amount
        self.sender = sender
        self.recipient = recipient
        self._status = "Инициализирован"  # Защищенное поле

    def execute(self):
        """
        Выполняет перевод и обновляет статус.
        """
        self._status = "Выполнен"
        print(f"Перевод на сумму {self.amount} от {self.sender} к {self.recipient} выполнен.")

    def _update_status(self, new_status):
        """
        Обновляет статус перевода (защищенный метод).
        
        Аргументы:
            new_status (str): Новый статус перевода.
        """
        self._status = new_status
        print(f"Статус перевода изменен на: {new_status}")

    def __private_method(self):
        """
        Закрытый метод, недоступный для внешнего использования.
        """
        print("Вызван закрытый метод __private_method.")


class PostalTransfer(MoneyTransfer):
    """
    Класс для почтовых переводов.
    
    Атрибуты:
        delivery_address (str): Адрес доставки перевода.
    """
    
    def __init__(self, amount, sender, recipient, delivery_address):
        """
        Инициализация класса PostalTransfer.
        
        Аргументы:
            amount (float): Сумма перевода.
            sender (str): Имя отправителя.
            recipient (str): Имя получателя.
            delivery_address (str): Адрес доставки перевода.
        """
        super().__init__(amount, sender, recipient)
        self.delivery_address = delivery_address

    def execute(self):
        """
        Выполняет почтовый перевод и выводит информацию о доставке.
        """
        super().execute()
        print(f"Почтовый перевод будет доставлен по адресу: {self.delivery_address}")


class BankTransfer(MoneyTransfer):
    """
    Класс для банковских переводов.
    
    Атрибуты:
        account_number (str): Номер счета получателя.
    """
    
    def __init__(self, amount, sender, recipient, account_number):
        """
        Инициализация класса BankTransfer.
        
        Аргументы:
            amount (float): Сумма перевода.
            sender (str): Имя отправителя.
            recipient (str): Имя получателя.
            account_number (str): Номер счета получателя.
        """
        super().__init__(amount, sender, recipient)
        self.account_number = account_number

    def execute(self):
        """
        Выполняет банковский перевод и выводит информацию о счете.
        """
        super().execute()
        print(f"Банковский перевод выполнен на счет: {self.account_number}")


class CurrencyTransfer(MoneyTransfer):
    """
    Класс для валютных переводов.
    
    Атрибуты:
        currency (str): Валюта перевода.
    """
    
    def __init__(self, amount, sender, recipient, currency):
        """
        Инициализация класса CurrencyTransfer.
        
        Аргументы:
            amount (float): Сумма перевода.
            sender (str): Имя отправителя.
            recipient (str): Имя получателя.
            currency (str): Валюта перевода.
        """
        super().__init__(amount, sender, recipient)
        self.currency = currency

    def execute(self):
        """
        Выполняет валютный перевод и выводит информацию о валюте.
        """
        super().execute()
        print(f"Валютный перевод выполнен в валюте: {self.currency}")


