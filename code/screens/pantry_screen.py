import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


class PantryScreen(tk.Frame):
    def __init__(self, parent, controller, green, red, items):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.items = items
        self.place(x=0, y=0, width=400, height=600)

        tk.Label(self, text="Моя кладовая", font=('Arial', 20, 'bold'), bg='white').pack(pady=20)

        # Таблица (убрана колонка 'Действия')
        columns = ('Продукт', 'Количество')  # Изменено
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=10)
        self.tree.heading('Продукт', text='Продукт')
        self.tree.heading('Количество', text='Количество')
        self.tree.column('Продукт', width=200)  # Расширил для компенсации
        self.tree.column('Количество', width=150)
        self.tree.pack(pady=20, padx=20, fill='both')

        self.update_table()

        # Кнопки действий (глобальные)
        self.change_btn = tk.Button(self, text='Изменить', bg=green, fg='white', command=self.change_item)
        self.change_btn.pack(pady=5)
        self.delete_btn = tk.Button(self, text='Удалить', bg=red, fg='white', command=self.delete_item)
        self.delete_btn.pack(pady=5)

        # Добавление (уже было, но уточнил лейблы)
        add_frame = tk.Frame(self)
        add_frame.pack(pady=10)
        tk.Label(add_frame, text="Название:", bg='white').pack(side='left')
        self.p_name = tk.Entry(add_frame, width=15)
        self.p_name.pack(side='left', padx=5)
        tk.Label(add_frame, text="Количество:", bg='white').pack(side='left', padx=5)
        self.p_amount = tk.Entry(add_frame, width=10)
        self.p_amount.pack(side='left', padx=5)
        tk.Button(add_frame, text="Добавить", bg=green, fg='white',
                  command=self.add_item).pack(side='left', padx=5)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.items:
            self.tree.insert('', 'end', values=(item['name'], item['amount']))  # Без 'Действия'

    def add_item(self):
        name = self.p_name.get()
        amount = self.p_amount.get()
        if name and amount:
            self.items.append({'name': name, 'amount': amount})
            self.controller.update_pantry_items(self.items)
            self.update_table()
            self.p_name.delete(0, tk.END)
            self.p_amount.delete(0, tk.END)
        else:
            messagebox.showwarning("Ошибка", "Заполните все поля!")

    def change_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите продукт!")
            return
        idx = self.tree.index(selected[0])
        new_amount = simpledialog.askstring("Изменить", "Новое количество:")
        if new_amount:
            self.items[idx]['amount'] = new_amount
            self.controller.update_pantry_items(self.items)
            self.update_table()

    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите продукт!")
            return
        idx = self.tree.index(selected[0])
        if messagebox.askyesno("Удалить", f"Удалить {self.items[idx]['name']}?"):
            del self.items[idx]
            self.controller.update_pantry_items(self.items)
            self.update_table()