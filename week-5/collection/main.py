from DateCollection import DateCollection
from date import Date

if __name__ == "__main__":
    
    collection = DateCollection()

    date1 = Date(15, 10, 2023)
    date2 = Date(25, 12, 2021)
    date3 = Date(30, 11, 2024)
    
    collection.add(date1)
    collection.add(date2)
    collection.add(date3)

    print("Содержимое коллекции")
    print(collection)  

    print("\nУдаление элемента")
    collection.remove(1)
    print(collection)
    
    print("\nСохранение коллекции в файл JSON")
    collection.save("dates.json")

    print("\nСоздание новой коллекции и загрузка из файла JSON")
    new_collection = DateCollection()
    new_collection.load("dates.json")
    print(new_collection)

# Пример использования:

# Содержимое коллекции
# [15.10.2023, 25.12.2021, 30.11.2024]

# Удаление элемента
# [15.10.2023, 31.11.2024]

# Сохранение коллекции в файл JSON

# Создание новой коллекции и загрузка из файла JSON      
# [15.10.2023, 31.11.2024]
