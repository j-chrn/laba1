import tkinter as tk
from tkinter import ttk, messagebox
from model import IncomeManager, ErrorLogger

class IncomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление доходами — Лабораторная 3")
        self.root.geometry("800x600")
        
        self.model = IncomeManager()
        self.filepath = "incomes.txt"
        
        self._setup_ui()
        self.model.load_from_file(self.filepath)
        self._refresh_all()

    def _setup_ui(self):
        # 1. Верхняя панель кнопок
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Button(toolbar, text="➕ Добавить", command=self._add_window).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="❌ Удалить", command=self._delete_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💾 Сохранить", command=self._save_data).pack(side=tk.LEFT, padx=2)

        # 2. Основная область (Разделение на две таблицы)
        main_container = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- СЕКЦИЯ ДАННЫХ (СВЕРХУ) ---
        data_frame = ttk.LabelFrame(main_container, text=" Список доходов ")
        main_container.add(data_frame, weight=3)

        cols = ("Дата", "Источник", "Сумма", "Цвет")
        self.data_tree = ttk.Treeview(data_frame, columns=cols, show="headings")
        for col in cols:
            self.data_tree.heading(col, text=col)
        self.data_tree.pack(fill=tk.BOTH, expand=True)

        # --- СЕКЦИЯ ОШИБОК (СНИЗУ) ---
        error_frame = ttk.LabelFrame(main_container, text=" Журнал ошибок и уведомлений ")
        main_container.add(error_frame, weight=1)

        err_cols = ("Время", "Сообщение об ошибке")
        self.error_tree = ttk.Treeview(error_frame, columns=err_cols, show="headings")
        self.error_tree.heading("Время", text="Время")
        self.error_tree.heading("Сообщение об ошибке", text="Сообщение об ошибке")
        self.error_tree.column("Время", width=100, stretch=False)
        
        # Настроим красный цвет для текста ошибок
        self.error_tree.tag_configure('error_row', foreground='red')
        self.error_tree.pack(fill=tk.BOTH, expand=True)

    def _refresh_all(self):
        """Обновляет обе таблицы."""
        # Обновление данных
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        for inc in self.model.incomes:
            self.data_tree.insert("", tk.END, values=inc.to_list())
        
        # Обновление логов
        for item in self.error_tree.get_children():
            self.error_tree.delete(item)
        for time_str, msg in ErrorLogger().history:
            self.error_tree.insert("", tk.END, values=(time_str, msg), tags=('error_row',))

    def _add_window(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Ввод данных")
        dialog.geometry("300x250")
        dialog.grab_set()

        fields = ["Дата (ГГГГ.ММ.ДД):", "Источник:", "Сумма:", "Цвет:"]
        entries = []
        for f in fields:
            ttk.Label(dialog, text=f).pack()
            e = ttk.Entry(dialog)
            e.pack(pady=2)
            entries.append(e)
        entries[0].insert(0, "2026.03.31")

        def submit():
            obj, err = self.model.add_income_safe(
                entries[0].get(), entries[1].get(), 
                entries[2].get(), entries[3].get()
            )
            self._refresh_all() # Обновит и таблицу, и лог снизу
            if not err:
                dialog.destroy()

        ttk.Button(dialog, text="Подтвердить", command=submit).pack(pady=10)

    def _delete_selected(self):
        selected = self.data_tree.selection()
        if selected:
            idx = self.data_tree.index(selected[0])
            del self.model.incomes[idx]
            self._refresh_all()

    def _save_data(self):
        self.model.save_to_file(self.filepath)
        messagebox.showinfo("Система", "Данные синхронизированы с файлом.")

if __name__ == "__main__":
    root = tk.Tk()
    app = IncomeApp(root)
    root.mainloop()