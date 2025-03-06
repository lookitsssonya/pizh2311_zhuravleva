from date import Date

# Создание объекта Date
date1 = Date(15, 10, 2023)
print(f"Дата 1: {date1}") # Результат: Дата 1: 15.10.2023

# Добавление дней
date2 = date1 + 10
print(f"Дата 1 + 10 дней: {date2}") # Результат: Дата 1 + 10 дней: 25.10.2023

# Вычитание дней
date3 = date2 - 5
print(f"Дата 2 - 5 дней: {date3}") # Результат: Дата 2 - 5 дней: 20.10.2023

# Сравнение дат
print(f"Дата 1 == Дата 3: {date1 == date3}") # Результат: Дата 1 == Дата 3: False
print(f"Дата 1 < Дата 3: {date1 < date3}") # Результат: Дата 1 < Дата 3: True

# Создание объекта из строки
date4 = Date.from_string("01.01.2024")
print(f"Дата: {date4}")  # Результат: Дата : 01.01.2024

# Сохранение и загрузка из JSON
date1.save("date1.json")
loaded_date = Date.load("date1.json")
print(f"Загруженная дата: {loaded_date}") # Результат: Загруженная дата: 15.10.2023

# Дополнительные методы
print(f"Високосный ли год: {date1.is_leap_year()}") # Результат: Високосный ли год: False
print(f"Количество дней в месяце: {date1.days_in_month()}") # Результат: Количество дней в месяце: 31