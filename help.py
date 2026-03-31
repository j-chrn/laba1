# -*- coding: utf-8 -*-
"""Модуль окна справки с изображением."""

import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk  # Необходимо установить: pip install Pillow


class HelpWindow(tk.Toplevel):
    """Окно справки с прокруткой и изображением."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("📖 СПРАВКА - Управление доходами")
        self.geometry("750x700")
        self.resizable(True, True)

        self._create_help_content()

    def _create_help_content(self):
        """Создает содержимое окна справки."""
        # Заголовок
        title_frame = tk.Frame(self, bg="#2196F3")
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(
            title_frame,
            text="📖 СПРАВКА ПО ПРОГРАММЕ",
            font=("Arial", 18, "bold"),
            bg="#2196F3",
            fg="white",
            pady=15
        )
        title_label.pack()

        # --- ДОБАВЛЕНИЕ КАРТИНКИ ---
        try:
            # Загружаем изображение (замените 'logo.png' на ваше имя файла)
            img = Image.open("logo.png")
            # При желании можно изменить размер:
            img = img.resize((100, 100), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            
            img_label = tk.Label(self, image=self.photo)
            img_label.pack(pady=10)
        except Exception as e:
            print(f"Не удалось загрузить изображение: {e}")
            # Если картинки нет, программа просто пойдет дальше
        # ---------------------------

        # Панель кнопок
        btn_frame = tk.Frame(self, bg="#e0e0e0")
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        btn_back = tk.Button(
            btn_frame,
            text="🔙 НАЗАД В МЕНЮ",
            command=self._go_back,
            width=25,
            height=2,
            font=("Arial", 11, "bold"),
            bg="#FF9800",
            fg="white",
            cursor="hand2"
        )
        btn_back.pack(side=tk.LEFT, padx=10, pady=5)

        btn_exit = tk.Button(
            btn_frame,
            text="🚪 ВЫХОД",
            command=self._exit_app,
            width=15,
            height=2,
            font=("Arial", 11, "bold"),
            bg="#f44336",
            fg="white",
            cursor="hand2"
        )
        btn_exit.pack(side=tk.RIGHT, padx=10, pady=5)

        text_frame = tk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            bg="white",
            padx=15,
            pady=15,
            spacing1=5,
            spacing3=5,
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Отредактированный текст без разработчика и года
        help_text = """
📋 ОПИСАНИЕ ПРОГРАММЫ

Программа предназначена для учета и управления личными доходами.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔘 ГЛАВНОЕ МЕНЮ

  💼 РАБОТАТЬ - Переход к окну управления доходами
  📖 СПРАВКА - Открывает это окно с информацией
  🚪 ВЫХОД - Закрывает программу

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💼 РАБОЧЕЕ ОКНО

  ➕ Добавить - Добавляет новый доход
  🗑️ Удалить - Удаляет выбранный доход
  🔄 Обновить - Перечитывает данные из файла
  💾 Сохранить - Сохраняет данные в файл
  🔙 НАЗАД - Возврат в главное меню

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 ФОРМАТ ДАННЫХ

Пример: Доход: 2024.01.15 "Зарплата" 50000 "Синий"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Программа: Управление доходами v2.0
"""

        self.text_area.insert(tk.END, help_text)
        self.text_area.config(state=tk.DISABLED)

        self.grab_set()

    def _go_back(self):
        self.destroy()
        self.parent._show_main_menu()

    def _exit_app(self):
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
            self.destroy()
            self.parent.destroy()