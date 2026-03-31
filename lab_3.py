# -*- coding: utf-8 -*-
import shlex
import os
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

        # Извлекаем данные после "Доход:"
        data = input_string[len(prefix):].strip()
        
        # --- ЛОГИКА ИЗ LAB_2: ПОДДЕРЖКА РАЗДЕЛИТЕЛЕЙ ---
        try:
            if ';' in data:
                # Разделяем по ; и очищаем от пробелов и лишних кавычек
                parts = [p.strip().strip('"').strip("'") for p in data.split(';')]
            else:
                # Используем shlex для стандартного формата с пробелами
                parts = shlex.split(data)
        except ValueError as e:
            raise IncomeFormatError(f"Ошибка парсинга (возможно, не закрыты кавычки): {e}")

        # Проверка количества полей
        if len(parts) != 4:
            raise IncomeFormatError(f"Неверное количество полей: ожидалось 4, получено {len(parts)}")

        try:
            # Преобразование типов данных
            date = datetime.strptime(parts[0], "%Y.%m.%d").date()
            amount = int(parts[2])
            return Income(date, parts[1], amount, parts[3])
        except ValueError as e:
            # Если дата 31 апреля или сумма не число — кидаем ошибку формата
            raise IncomeFormatError(f"Ошибка преобразования типов данных: {e}")

    @staticmethod
    def read_from_file(filepath: str) -> List[Income]:
        incomes = []
        if not os.path.exists(filepath):
            return incomes
            
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line: 
                        continue
                    try:
                        incomes.append(IncomeFileReader.parse_income(line))
                    except IncomeError as e:
                        # В Lab 3 ошибки выводятся в консоль как логи
                        print(f"[LOG][Строка {line_num}]: {e} | Содержимое: '{line}'")
        except Exception as e:
            print(f"Критическая ошибка при чтении файла: {e}")
            
        return incomes

    @staticmethod
    def format_income(income: Income) -> str:
        """Форматирует объект для записи в файл (используем стандартный формат)."""
        return f'Доход: {income.date.strftime("%Y.%m.%d")} "{income.source}" {income.amount} "{income.color}"'

    @staticmethod
    def write_to_file(filepath: str, incomes: List[Income]) -> None:
        """Сохраняет данные в файл."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for inc in incomes:
                    f.write(IncomeFileReader.format_income(inc) + '\n')
        except Exception as e:
            print(f"Ошибка при записи в файл: {e}")