import shlex
import os
from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple, Optional

# --- ПАТТЕРН SINGLETON ДЛЯ ЛОГГЕРА ---
class ErrorLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ErrorLogger, cls).__new__(cls)
            cls._instance.log_file = "Log.txt"
            # Храним список кортежей (время, сообщение) для таблицы в GUI
            cls._instance.history: List[Tuple[str, str]] = []
        return cls._instance

    def log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        date_stamp = datetime.now().strftime("%Y-%m-%d")
        
        # Запись в текстовый файл (полный лог)
        full_entry = f"[{date_stamp} {timestamp}] ERROR: {message}"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(full_entry + "\n")
        
        # Сохранение в оперативную память для таблицы в окне
        self.history.append((timestamp, message))

@dataclass
class Income:
    date: datetime.date
    source: str
    amount: int
    color: str

    def to_list(self) -> List[str]:
        return [self.date.strftime('%Y.%m.%d'), self.source, str(self.amount), self.color]

class IncomeManager:
    def __init__(self):
        self.incomes: List[Income] = []
        self.logger = ErrorLogger()

    # --- ПАТТЕРН (obj, error) ---
    def add_income_safe(self, date_str: str, source: str, amount_str: str, color: str) -> Tuple[Optional[Income], Optional[str]]:
        try:
            if not source.strip():
                return None, "Пустое поле 'Источник'"
            
            date = datetime.strptime(date_str, "%Y.%m.%d").date()
            amount = int(amount_str)
            
            if amount < 0:
                return None, "Сумма не может быть отрицательной"
            
            new_inc = Income(date, source, amount, color)
            self.incomes.append(new_inc)
            return new_inc, None
            
        except ValueError:
            err_msg = f"Некорректный ввод данных: {date_str}, {amount_str}"
            self.logger.log(err_msg)
            return None, err_msg

    def parse_line_safe(self, line: str) -> Tuple[Optional[Income], Optional[str]]:
        prefix = "Доход:"
        if not line.startswith(prefix):
            return None, "Неверный префикс (должен быть 'Доход:')"

        try:
            data = line[len(prefix):].strip()
            parts = shlex.split(data)
            if len(parts) != 4:
                return None, f"Ожидалось 4 поля, найдено {len(parts)}"
            
            date = datetime.strptime(parts[0], "%Y.%m.%d").date()
            amount = int(parts[2])
            return Income(date, parts[1], amount, parts[3]), None
        except Exception as e:
            return None, str(e)

    def load_from_file(self, filepath: str):
        self.incomes = []
        if not os.path.exists(filepath): return
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line: continue
                
                obj, err = self.parse_line_safe(line)
                if obj:
                    self.incomes.append(obj)
                else:
                    self.logger.log(f"Файл, стр {i}: {err}")