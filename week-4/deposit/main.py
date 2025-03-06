from deposit import deposits

if __name__ == "__main__":
    print("Добро пожаловать в систему подбора вкладов!")

    while True:
        print("\n-----")
        print("Нажмите 1, чтобы подобрать вклад, или что угодно для выхода.")

        answer = input()
        if answer == "1":
            initial_sum = float(input("1/2: Введите начальную сумму вклада: "))
            period = int(input("2/2: Введите срок вклада (мес.): "))

            matched_deposits = []
            for deposit in deposits:
                try:
                    deposit._check_user_params(initial_sum, period)
                    matched_deposits.append(deposit)
                except AssertionError as err:
                    pass

            if len(matched_deposits) > 0:
                print("{0:18} | {1:13} | {2:13}".format(
                    "Вклад", "Прибыль", "Итоговая сумма"
                ))
                for deposit in matched_deposits:
                    print("{0:18} | {1:8,.2f} {3:4} | {2:8,.2f} {3:4}".format(
                          deposit.name,
                          deposit.get_profit(initial_sum, period),
                          deposit.get_sum(initial_sum, period),
                          deposit.currency))
            else:
                print("К сожалению, нет подходящих Вам вкладов.")

        else:
            break

    print("\nСпасибо, что воспользовались терминалом банка! До встречи!")
  
  
    
""" Пример вывода: 
Добро пожаловать в систему подбора вкладов!

-----
Нажмите 1, чтобы подобрать вклад, или что угодно для выхода.   
1   
1/2: Введите начальную сумму вклада: 50000   
2/2: Введите срок вклада (мес.): 8   
Вклад              | Прибыль       | Итоговая сумма    
Сохраняй           | 1,666.67 руб. | 51,666.67 руб.    
Бонусный 2         | 1,750.00 руб. | 51,750.00 руб.    
С капитализацией   | 1,691.18 руб. | 51,691.18 руб.    

-----
Нажмите 1, чтобы подобрать вклад, или что угодно для выхода.    
1    
1/2: Введите начальную сумму вклада: 100000    
2/2: Введите срок вклада (мес.): 3    
К сожалению, нет подходящих Вам вкладов. """