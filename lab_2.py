# -*- coding: utf-8 -*-


import shlex
import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from typing import List, Optional


class Income:
    """Класс, представляющий объект дохода."""

    def __init__(self, date: datetime.date, source: str, amount: int, color: str) -> None:
        self.date = date
        self.source = source
        self.amount = amount
        self.color = color

    def to_list(self) -> List[str]:
        """Преобразует данные объекта в список строк для таблицы."""
        return [
            self.date.strftime('%Y.%m.%d'),
            self.source,
            str(self.amount),
            self.color
        ]


class IncomeFileReader:
    """Класс для работы с файловой системой и парсинга данных."""

    @staticmethod
    def _parse_line(data_str: str) -> List[str]:
        
        data_str = data_str.strip()
        
        
        if ';' in data_str:
            
            parts = [p.strip().strip('"').strip("'") for p in data_str.split(';')]
        else:
            
            parts = shlex.split(data_str)
            
        return parts

    @staticmethod
    def read_from_file(filepath: str) -> List[Income]:
        """Читает файл и создает список объектов Income."""
        incomes = []
        if not os.path.exists(filepath):
            return incomes

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or not line.startswith("Доход:"):
                        continue
                    
                    # Получаем часть строки после "Доход:"
                    raw_content = line[len("Доход:"):].strip()
                    
                    # Вызываем наш обновленный парсер
                    parts = IncomeFileReader._parse_line(raw_content)

                    # Проверяем, что получили ровно 4 колонки данных
                    if len(parts) == 4:
                        try:
                            date = datetime.strptime(parts[0], '%Y.%m.%d').date()
                            incomes.append(Income(
                                date=date,
                                source=parts[1],
                                amount=int(parts[2]),
                                color=parts[3]
                            ))
                        except ValueError:
                            continue 
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            
        return incomes

    @staticmethod
    def write_to_file(filepath: str, incomes: List[Income]) -> None:
        """Сохраняет список доходов обратно в файл (в стандартном формате)."""
        with open(filepath, 'w', encoding='utf-8') as f:
            for inc in incomes:
                # Сохраняем в кавычках для надежности (формат по пробелам)
                f.write(f'Доход: {inc.date.strftime("%Y.%m.%d")} "{inc.source}" {inc.amount} "{inc.color}"\n')


class IncomeApp:
    """Класс графического интерфейса приложения."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Учет доходов (Lab 2)")
        self.root.geometry("750x500")
        
        self.filepath = "incomes.txt"
        self.incomes: List[Income] = []
        
        self._setup_ui()
        self._load_data()

    def _setup_ui(self) -> None:
        """Создание интерфейса."""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Button(toolbar, text="➕ Добавить", command=self._open_add_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="❌ Удалить", command=self._delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="💾 Сохранить", command=self._save_to_file).pack(side=tk.LEFT, padx=5)

        cols = ("Дата", "Источник", "Сумма", "Цвет")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _load_data(self) -> None:
        self.incomes = IncomeFileReader.read_from_file(self.filepath)
        self._update_table()

    def _save_to_file(self) -> None:
        IncomeFileReader.write_to_file(self.filepath, self.incomes)
        messagebox.showinfo("Успех", "Данные сохранены в файл!")

    def _update_table(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
        for inc in self.incomes:
            self.tree.insert("", tk.END, values=inc.to_list())

    def _open_add_dialog(self) -> None:
        dialog = tk.Toplevel(self.root)
        dialog.title("Новая запись")
        dialog.geometry("300x280")
        dialog.grab_set()

        fields = ["Дата (ГГГГ.ММ.ДД):", "Источник:", "Сумма:", "Цвет:"]
        entries = []
        for text in fields:
            ttk.Label(dialog, text=text).pack(pady=(5, 0))
            entry = ttk.Entry(dialog)
            entry.pack(pady=2)
            entries.append(entry)
        
        entries[0].insert(0, datetime.now().strftime('%Y.%m.%d'))

        def save():
            try:
                new_date = datetime.strptime(entries[0].get(), '%Y.%m.%d').date()
                new_inc = Income(
                    date=new_date,
                    source=entries[1].get(),
                    amount=int(entries[2].get()),
                    color=entries[3].get()
                )
                self.incomes.append(new_inc)
                self._update_table()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат данных!")

        ttk.Button(dialog, text="Добавить", command=save).pack(pady=15)

    def _delete_selected(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите строку")
            return
        
        idx = self.tree.index(selected[0])
        del self.incomes[idx]
        self._update_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = IncomeApp(root)
    root.mainloop()