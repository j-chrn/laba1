# -*- coding: utf-8 -*-
"""Модуль главного меню приложения."""

import tkinter as tk
from tkinter import messagebox


class MainMenu(tk.Tk):
    """Главное меню программы управления доходами."""

    def __init__(self):
        super().__init__()
        self.title("Главное меню - Управление доходами")
        self.geometry("450x400")
        self.resizable(False, False)
        self._create_menu()

    def _create_menu(self):
        """Создает элементы главного меню."""
        # Заголовок
        title_label = tk.Label(
            self,
            text="💰 УПРАВЛЕНИЕ ДОХОДАМИ",
            font=("Arial", 18, "bold"),
            fg="#2E7D32"
        )
        title_label.pack(pady=30)

        # Подзаголовок
        subtitle_label = tk.Label(
            self,
            text="Система учета личных финансов",
            font=("Arial", 11),
            fg="gray"
        )
        subtitle_label.pack(pady=(0, 30))

        # Фрейм для кнопок
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        # Кнопка РАБОТАТЬ
        btn_work = tk.Button(
            button_frame,
            text="💼 РАБОТАТЬ",
            command=self._open_work_window,
            width=30,
            height=2,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            cursor="hand2"
        )
        btn_work.pack(pady=8)

        # Кнопка СПРАВКА
        btn_help = tk.Button(
            button_frame,
            text="📖 СПРАВКА",
            command=self._open_help_window,
            width=30,
            height=2,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
            cursor="hand2"
        )
        btn_help.pack(pady=8)

        # Кнопка ВЫХОД
        btn_exit = tk.Button(
            button_frame,
            text="🚪 ВЫХОД",
            command=self._exit_app,
            width=30,
            height=2,
            font=("Arial", 12, "bold"),
            bg="#f44336",
            fg="white",
            cursor="hand2"
        )
        btn_exit.pack(pady=8)

        # Футер с информацией
        footer_label = tk.Label(
            self,
            text="Разработчик: Студент ПИ-31\nУправление доходами v2.0",
            font=("Arial", 9),
            fg="gray",
            justify=tk.CENTER
        )
        footer_label.pack(side=tk.BOTTOM, pady=15)

    def _open_work_window(self):
        """Открывает рабочее окно с таблицей доходов."""
        from gui_work import WorkWindow
        self.withdraw()  # Скрываем главное меню
        work_window = WorkWindow(self)

    def _open_help_window(self):
        """Открывает окно справки."""
        from help import HelpWindow
        self.withdraw()  # Скрываем главное меню
        help_window = HelpWindow(self)

    def _show_main_menu(self):
        """Показывает главное меню."""
        self.deiconify()

    def _exit_app(self):
        """Закрывает приложение с подтверждением."""
        if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
            self.destroy()


# Для тестирования отдельно
if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()