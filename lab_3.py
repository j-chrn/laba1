# -*- coding: utf-8 -*-
import shlex
from datetime import datetime
from typing import List

class IncomeError(Exception):
    """Базовое исключение для ошибок в модуле Income."""
    pass

class IncomeFormatError(IncomeError):
    """Ошибка формата строки в файле."""
    pass

class Income:
    def __init__(self, date: datetime.date, source: str, amount: int, color: str) -> None:
        if amount < 0:
            raise ValueError("Сумма дохода не может быть отрицательной")
        self.date = date
        self.source = source
        self.amount = amount
        self.color = color

    def to_list(self) -> List[str]:
        return [self.date.strftime('%Y.%m.%d'), self.source, str(self.amount), self.color]

class IncomeFileReader:
    @staticmethod
    def parse_income(input_string: str) -> Income:
        prefix = "Доход:"
        if not input_string.startswith(prefix):
            raise IncomeFormatError(f"Строка должна начинаться с '{prefix}'")

        data = input_string[len(prefix):].strip()
        try:
            parts = shlex.split(data)
        except ValueError as e:
            raise IncomeFormatError(f"Ошибка парсинга кавычек: {e}")

        if len(parts) != 4:
            raise IncomeFormatError(f"Ожидалось 4 аргумента, получено {len(parts)}")

        try:
            date = datetime.strptime(parts[0], "%Y.%m.%d").date()
            amount = int(parts[2])
            return Income(date, parts[1], amount, parts[3])
        except ValueError as e:
            raise IncomeFormatError(f"Ошибка преобразования типов: {e}")

    @staticmethod
    def read_from_file(filepath: str) -> List[Income]:
        incomes = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line: continue
                    try:
                        incomes.append(IncomeFileReader.parse_income(line))
                    except IncomeError as e:
                        # Логирование ошибок (в консоль или файл)
                        print(f"[LOG][Строка {line_num}]: {e} | Содержимое: '{line}'")
        except FileNotFoundError:
            print(f"Файл {filepath} не найден")
        return incomes

    @staticmethod
    def format_income(income: Income) -> str:
        return f'Доход: {income.date.strftime("%Y.%m.%d")} {shlex.quote(income.source)} {income.amount} {shlex.quote(income.color)}'

    @staticmethod
    def write_to_file(filepath: str, incomes: List[Income]) -> None:
        with open(filepath, 'w', encoding='utf-8') as file:
            for inc in incomes:
                file.write(IncomeFileReader.format_income(inc) + '\n')