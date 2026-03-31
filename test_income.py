import unittest
from model import IncomeManager, ErrorLogger

class TestIncomeSystem(unittest.TestCase):
    def setUp(self):
        self.manager = IncomeManager()
        ErrorLogger().history = [] # Очистка логов перед каждым тестом

    def test_singleton_logger(self):
        """Проверка паттерна Singleton."""
        logger1 = ErrorLogger()
        logger2 = ErrorLogger()
        self.assertIs(logger1, logger2)

    def test_error_pattern_fail(self):
        """Проверка паттерна (obj, error) при ошибке."""
        obj, err = self.manager.add_income_safe("wrong-date", "Test", "abc", "Red")
        self.assertIsNone(obj)
        self.assertIsNotNone(err)
        # Проверяем, попала ли ошибка в синглтон-логгер
        self.assertTrue(len(ErrorLogger().history) > 0)

    def test_add_success(self):
        """Проверка успешного добавления."""
        obj, err = self.manager.add_income_safe("2026.01.01", "Freelance", "1000", "Blue")
        self.assertIsNotNone(obj)
        self.assertIsNone(err)

if __name__ == "__main__":
    unittest.main()