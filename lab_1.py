from datetime import datetime
import shlex


class Income:
    def __init__(self, date, source, amount, color):
        self.date = date
        self.source = source
        self.amount = amount
        self.color = color

    def __str__(self):
        return (
            "Объект типа 'Доход'\n"
            f"Дата: {self.date.strftime('%Y.%m.%d')}\n"
            f"Источник: {self.source}\n"
            f"Сумма: {self.amount}\n"
            f"Цвет: {self.color}\n"
        )


def parse_income(input_string):
    prefix = "Доход:"
    if not input_string.startswith(prefix):
        raise ValueError

    data = input_string[len(prefix):].strip()
    parts = shlex.split(data)

    if len(parts) != 4:
        raise ValueError

    date_str, source, amount_str, color = parts

    date = datetime.strptime(date_str, "%Y.%m.%d").date()
    amount = int(amount_str)

    return Income(date, source, amount, color)


if __name__ == "__main__":
    incomes = []

    while True:
        print("\nМеню:")
        print("1 — Добавить доход")
        print("2 — Вывести все доходы")
        print("0 — Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            user_input = input(
                "Введите данные в формате:\n"
                "Доход: ГГГГ.ММ.ДД \"Источник\" Сумма \"Цвет\"\n"
            )
            income = parse_income(user_input)
            incomes.append(income)
            print("Доход добавлен.")

        elif choice == "2":
            if not incomes:
                print("Список доходов пуст.")
            else:
                print()
                for income in incomes:
                    print(income)

        elif choice == "0":
            print("Программа завершена.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")