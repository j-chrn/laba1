# -*- coding: utf-8 -*-
import unittest
import tkinter as tk
from tkinter import ttk
import os
from main1 import IncomeApp
from model import ErrorLogger

class TestLab3UI(unittest.TestCase):
    def setUp(self):
        """Настройка окружения перед каждым тестом."""
        self.root = tk.Tk()
        self.app = IncomeApp(self.root)
        self.test_file = "incomes.txt"
        # Очищаем логи перед тестом
        ErrorLogger().history = []

    def tearDown(self):
        """Очистка после завершения теста."""
        self.root.update()
        self.root.destroy()

    def test_app_initialization(self):
        """Проверка инициализации: заголовок и наличие таблиц."""
        self.assertEqual(self.root.title(), "Управление доходами — Лабораторная 3")
        # Проверяем, что созданы обе таблицы
        self.assertTrue(hasattr(self.app, 'data_tree'))
        self.assertTrue(hasattr(self.app, 'error_tree'))

    def test_invalid_data_logging(self):
        """Тест Lab 3: проверка, что некорректные данные попадают в лог ошибок."""
        # Имитируем открытие окна добавления и ввод заведомо ложных данных
        # Вместо ручного ввода вызовем метод модели через интерфейс, как это делает кнопка
        invalid_date = "2026.13.01" # Несуществующий месяц
        
        self.app.model.add_income_safe(invalid_date, "Тест", "1000", "Красный")
        self.app._refresh_all()
        
        # Проверяем, что в таблице ошибок (error_tree) появилась запись
        error_rows = self.app.error_tree.get_children()
        self.assertGreater(len(error_rows), 0, "Ошибка не была зафиксирована в UI таблице ошибок")
        
        # Проверяем текст ошибки в таблице
        error_text = self.app.error_tree.item(error_rows[0])['values'][1]
        self.assertIn("Некорректный ввод", error_text)

    def test_successful_addition(self):
        """Проверка успешного добавления корректной записи."""
        initial_count = len(self.app.data_tree.get_children())
        
        # Добавляем валидные данные
        self.app.model.add_income_safe("2026.04.01", "Зарплата", "50000", "Зеленый")
        self.app._refresh_all()
        
        new_count = len(self.app.data_tree.get_children())
        self.assertEqual(new_count, initial_count + 1, "Запись не добавилась в основную таблицу")

    def test_delete_functionality(self):
        """Проверка удаления выбранной записи."""
        # Сначала добавим запись
        self.app.model.add_income_safe("2026.04.01", "Удаление", "100", "Серый")
        self.app._refresh_all()
        
        # Выделяем первую строку в таблице
        first_item = self.app.data_tree.get_children()[0]
        self.app.data_tree.selection_set(first_item)
        
        # Вызываем удаление
        self.app._delete_selected()
        
        # Проверяем, что запись исчезла
        self.assertNotIn(first_item, self.app.data_tree.get_children())

if __name__ == "__main__":
    unittest.main()