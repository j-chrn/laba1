# -*- coding: utf-8 -*-
"""Модуль для управления доходами с графическим интерфейсом."""

import shlex
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from typing import List


class Income:
    """Класс, представляющий доход."""

    def __init__(self, date: datetime.date, source: str, amount: int, color: str) -> None:
        """Инициализирует объект дохода."""
        self.date = date
        self.source = source
        self.amount = amount
        self.color = color

    def __str__(self) -> str:
        """Возвращает строковое представление дохода."""
        return (
            "Объект типа 'Доход'\n"
            f"Дата: {self.date.strftime('%Y.%m.%d')}\n"
            f"Источник: {self.source}\n"
            f"Сумма: {self.amount}\n"
            f"Цвет: {self.color}"
        )

    def to_list(self) -> List[str]:
        """Преобразует доход в список строк для отображения в таблице."""
        return [
            self.date.strftime('%Y.%m.%d'),
            self.source,
            str(self.amount),
            self.color
        ]


class IncomeFileReader:
    """Класс для чтения доходов из файла."""

    @staticmethod
    def parse_income(input_string: str) -> Income:
        """Разбирает строку и создает объект Income."""
        prefix = "Доход:"
        if not input_string.startswith(prefix):
            raise ValueError("Строка должна начинаться с 'Доход:'")

        data = input_string[len(prefix):].strip()
        parts = shlex.split(data)

        if len(parts) != 4:
            raise ValueError("Требуется 4 аргумента: дата, источник, сумма, цвет")

        date_str, source, amount_str, color = parts
        date = datetime.strptime(date_str, "%Y.%m.%d").date()
        amount = int(amount_str)

        return Income(date, source, amount, color)

    @staticmethod
    def read_from_file(filepath: str) -> List[Income]:
        """Читает все доходы из файла."""
        incomes = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        try:
                            income = IncomeFileReader.parse_income(line)
                            incomes.append(income)
                        except ValueError as e:
                            print(f"Пропущена строка: {line} - {e}")
        except FileNotFoundError:
            print(f"Файл {filepath} не найден")
        return incomes

    @staticmethod
    def format_income(income: Income) -> str:
        """Форматирует доход для записи в файл."""
        return (
            f'Доход: {income.date.strftime("%Y.%m.%d")} '
            f'{shlex.quote(income.source)} {income.amount} '
            f'{shlex.quote(income.color)}'
        )

    @staticmethod
    def write_to_file(filepath: str, incomes: List[Income]) -> None:
        """Записывает список доходов в файл."""
        with open(filepath, 'w', encoding='utf-8') as file:
            for income in incomes:
                file.write(IncomeFileReader.format_income(income) + '\n')


class IncomeApp:
    """Главное окно приложения для управления доходами."""

    def __init__(self, root: tk.Tk, filepath: str = "incomes.txt") -> None:
        """Инициализирует приложение."""
        self.root = root
        self.filepath = filepath
        self.incomes: List[Income] = []
        self.tree = None

        self._setup_window()
        self._create_widgets()
        self._load_data()

    def _setup_window(self) -> None:
        """Настраивает параметры главного окна."""
        self.root.title("Управление доходами")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

    def _create_widgets(self) -> None:
        """Создает все виджеты интерфейса."""
        # Фрейм для таблицы
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Создание таблицы
        columns = ("Дата", "Источник", "Сумма", "Цвет")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # Настройка заголовков
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # Скроллбары
        v_scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        h_scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Размещение таблицы и скроллбаров
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Фрейм для кнопок
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            button_frame,
            text="Добавить доход",
            command=self._show_add_dialog
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Удалить выделенный",
            command=self._delete_selected
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Обновить из файла",
            command=self._load_data
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Сохранить в файл",
            command=self._save_data
        ).pack(side=tk.LEFT, padx=5)

    def _load_data(self) -> None:
        """Загружает данные из файла и обновляет таблицу."""
        self.incomes = IncomeFileReader.read_from_file(self.filepath)
        self._refresh_table()
        
        if not self.incomes:
            messagebox.showinfo(
                "Нет данных",
                f"Файл {self.filepath} пуст или не содержит корректных данных.\n"
                "Вы можете добавить доходы через интерфейс."
            )

    def _save_data(self) -> None:
        """Сохраняет текущий список доходов в файл."""
        try:
            IncomeFileReader.write_to_file(self.filepath, self.incomes)
            messagebox.showinfo("Успех", "Данные сохранены в файл")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def _refresh_table(self) -> None:
        """Обновляет отображение таблицы."""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение таблицы
        for income in self.incomes:
            self.tree.insert("", tk.END, values=income.to_list())

    def _delete_selected(self) -> None:
        """Удаляет выделенный в таблице доход."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Нет выделения", "Пожалуйста, выберите доход для удаления")
            return

        # Получаем индекс выделенного элемента
        item = selected[0]
        index = self.tree.index(item)

        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", "Удалить выбранный доход?"):
            del self.incomes[index]
            self._refresh_table()

    def _show_add_dialog(self) -> None:
        """Показывает диалог добавления дохода."""
        # FIXED: Создаем диалог как дочернее окно
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление дохода")
        dialog.geometry("400x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)  # Связываем с главным окном
        dialog.grab_set()  # Захватываем фокус
        dialog.focus_set()  # Устанавливаем фокус

        # FIXED: Создаем фрейм для лучшего расположения
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Поля ввода
        ttk.Label(main_frame, text="Дата (ГГГГ.ММ.ДД):").pack(anchor=tk.W, pady=(0, 5))
        date_entry = ttk.Entry(main_frame, width=35)
        date_entry.pack(fill=tk.X, pady=(0, 10))
        date_entry.insert(0, datetime.now().strftime("%Y.%m.%d"))  # FIXED: Подставляем текущую дату

        ttk.Label(main_frame, text="Источник:").pack(anchor=tk.W, pady=(0, 5))
        source_entry = ttk.Entry(main_frame, width=35)
        source_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(main_frame, text="Сумма (целое число):").pack(anchor=tk.W, pady=(0, 5))
        amount_entry = ttk.Entry(main_frame, width=35)
        amount_entry.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(main_frame, text="Цвет:").pack(anchor=tk.W, pady=(0, 5))
        color_entry = ttk.Entry(main_frame, width=35)
        color_entry.pack(fill=tk.X, pady=(0, 10))

        # FIXED: Функция добавления с доступом к переменным
        def add_income():
            """Обработчик добавления дохода."""
            try:
                # Получаем значения из полей
                date_str = date_entry.get().strip()
                source = source_entry.get().strip()
                amount_str = amount_entry.get().strip()
                color = color_entry.get().strip()

                # Проверка на пустые поля
                if not date_str:
                    raise ValueError("Дата не может быть пустой")
                if not source:
                    raise ValueError("Источник не может быть пустым")
                if not amount_str:
                    raise ValueError("Сумма не может быть пустой")
                if not color:
                    raise ValueError("Цвет не может быть пустым")

                # Парсим данные
                date = datetime.strptime(date_str, "%Y.%m.%d").date()
                amount = int(amount_str)

                # Создаем доход и добавляем
                income = Income(date, source, amount, color)
                self.incomes.append(income)
                self._refresh_table()
                
                # Закрываем диалог
                dialog.destroy()
                
                # Показываем сообщение об успехе
                messagebox.showinfo("Успех", "Доход успешно добавлен!")

            except ValueError as e:
                messagebox.showerror("Ошибка ввода", f"Неверный формат данных:\n{e}")

        # FIXED: Кнопка с правильной привязкой
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Добавить",
            command=add_income,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Отмена",
            command=dialog.destroy,
            width=15
        ).pack(side=tk.RIGHT, padx=5)
        
        # FIXED: Привязываем Enter к добавлению
        dialog.bind('<Return>', lambda event: add_income())


def create_sample_file_if_not_exists(filepath: str) -> None:
    """Создает пример файла с данными, если он не существует."""
    import os
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('Доход: 2024.01.15 "Зарплата" 50000 "Синий"\n')
            f.write('Доход: 2024.01.20 "Фриланс" 15000 "Зеленый"\n')
            f.write('Доход: 2024.02.01 "Дивиденды" 8000 "Желтый"\n')
        print(f"Создан пример файла: {filepath}")


def main() -> None:
    """Главная функция запуска приложения."""
    create_sample_file_if_not_exists("incomes.txt")
    root = tk.Tk()
    app = IncomeApp(root, "incomes.txt")
    root.mainloop()


if __name__ == "__main__":
    main()