# test_all.py - для проверки всех импортов
import sys
print("Проверка импортов...")

try:
    from lab_2 import Income, IncomeFileReader
    print("✅ lab_2 - OK")
except Exception as e:
    print(f"❌ lab_2: {e}")

try:
    from gui_menu import MainMenu
    print("✅ gui_menu - OK")
except Exception as e:
    print(f"❌ gui_menu: {e}")

try:
    from gui_work import WorkWindow
    print("✅ gui_work - OK")
except Exception as e:
    print(f"❌ gui_work: {e}")

try:
    from help import HelpWindow
    print("✅ help - OK")
except Exception as e:
    print(f"❌ help: {e}")

print("\nПопытка запуска приложения...")
try:
    app = MainMenu()
    app.mainloop()
except Exception as e:
    print(f"Ошибка запуска: {e}")