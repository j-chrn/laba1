# -*- coding: utf-8 -*-
"""Модуль рабочего окна с таблицей доходов."""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from lab_2 import Income, IncomeFileReader


class WorkWindow(tk.Toplevel):
    """Рабочее окно с таблицей доходов."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Управление доходами - Рабочее окно")
        self.geometry("800x600")
        self.resizable(True, True)

        self.storage_reader = IncomeFileReader()
        self.incomes = []
        self.filepath = "incomes.txt"

        self._create_widgets()
        self._load_data()

    def _create_widgets(self):
        """Создает все виджеты рабочего окна."""
        # Заголовок
        title_frame = tk.Frame(self, bg="#2E7D32", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="💰 УПРАВЛЕНИЕ ДОХОДАМИ",
            font=("Arial", 16, "bold"),
            bg="#2E7D32",
            fg="white"
        )
        title_label.pack(expand=True)

        # Основной фрейм
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Таблица
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Дата", "Источник", "Сумма", "Цвет")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse",
            height=12
        )

        # Настройка заголовков
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.column("Источник", width=250)

        # Скроллбары
        v_scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        h_scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(main_frame, text="Добавление нового дохода", padding="10")
        input_frame.pack(fill=tk.X, pady=10)

        # Поля ввода
        fields_frame = ttk.Frame(input_frame)
        fields_frame.pack(fill=tk.X)

        # Дата
        ttk.Label(fields_frame, text="Дата (ГГГГ.ММ.ДД):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_date = ttk.Entry(fields_frame, width=15)
        self.entry_date.grid(row=0, column=1, padx=5, pady=5)
        self.entry_date.insert(0, datetime.now().strftime("%Y.%m.%d"))

        # Источник
        ttk.Label(fields_frame, text="Источник:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_source = ttk.Entry(fields_frame, width=20)
        self.entry_source.grid(row=0, column=3, padx=5, pady=5)

        # Сумма
        ttk.Label(fields_frame, text="Сумма (руб):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_amount = ttk.Entry(fields_frame, width=15)
        self.entry_amount.grid(row=1, column=1, padx=5, pady=5)

        # Цвет
        ttk.Label(fields_frame, text="Цвет:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_color = ttk.Entry(fields_frame, width=20)
        self.entry_color.grid(row=1, column=3, padx=5, pady=5)

        # Кнопки управления
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            btn_frame,
            text="➕ Добавить",
            command=self._add_item,
            width=12
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="🗑️ Удалить выделенный",
            command=self._delete_item,
            width=18
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="🔄 Обновить из файла",
            command=self._load_data,
            width=18
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="💾 Сохранить в файл",
            command=self._save_data,
            width=18
        ).pack(side=tk.LEFT, padx=5)

        # Панель навигации
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X, pady=10)

        btn_back = tk.Button(
            nav_frame,
            text="🔙 НАЗАД В МЕНЮ",
            command=self._go_back,
            width=20,
            height=2,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        btn_back.pack(side=tk.LEFT, padx=10)

        btn_exit = tk.Button(
            nav_frame,
            text="🚪 ВЫХОД",
            command=self._exit_app,
            width=15,
            height=2,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        btn_exit.pack(side=tk.RIGHT, padx=10)

        # Строка статуса
        self.status_var = tk.StringVar()
        status_bar = tk.Label(
            self,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _load_data(self):
        """Загружает данные из файла."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.incomes = self.storage_reader.read_from_file(self.filepath)

        for income in self.incomes:
            self.tree.insert("", tk.END, values=income.to_list())

        self.status_var.set(f"📊 Загружено: {len(self.incomes)} доходов")

    def _add_item(self):
        """Добавляет новый доход."""
        try:
            date_str = self.entry_date.get().strip()
            source = self.entry_source.get().strip()
            amount_str = self.entry_amount.get().strip()
            color = self.entry_color.get().strip()

            if not date_str or not source or not amount_str or not color:
                raise ValueError("Все поля должны быть заполнены")

            date = datetime.strptime(date_str, "%Y.%m.%d").date()
            amount = int(amount_str)

            new_income = Income(date, source, amount, color)
            self.incomes.append(new_income)

            self.tree.insert("", tk.END, values=new_income.to_list())

            self.entry_source.delete(0, tk.END)
            self.entry_amount.delete(0, tk.END)
            self.entry_color.delete(0, tk.END)

            self.status_var.set(f"✅ Добавлен доход: {source} - {amount} руб.")
            messagebox.showinfo("Успех", "Доход успешно добавлен!")

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", f"Неверный формат данных:\n{e}")

    def _delete_item(self):
        """Удаляет выделенный доход."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите доход для удаления")
            return

        if messagebox.askyesno("Подтверждение", "Удалить выбранный доход?"):
            indices = [self.tree.index(item) for item in selected]
            indices.sort(reverse=True)

            for index in indices:
                del self.incomes[index]

            self._refresh_table()
            self.status_var.set(f"🗑️ Удалено {len(indices)} доходов")

    def _save_data(self):
        """Сохраняет данные в файл."""
        try:
            self.storage_reader.write_to_file(self.filepath, self.incomes)
            messagebox.showinfo("Сохранение", "Данные сохранены в файл!")
            self.status_var.set(f"💾 Данные сохранены в {self.filepath}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def _refresh_table(self):
        """Обновляет таблицу."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for income in self.incomes:
            self.tree.insert("", tk.END, values=income.to_list())

    def _go_back(self):
        """Возвращается в главное меню."""
        self.destroy()
        self.parent._show_main_menu()

    def _exit_app(self):
        """Закрывает программу."""
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
            self.destroy()
            self.parent.destroy()
