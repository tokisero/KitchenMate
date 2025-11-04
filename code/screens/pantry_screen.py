import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from config import TITLE_FONT, BODY_FONT


class PantryScreen(tk.Frame):
    def __init__(self, parent, controller, green, red, items):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.green = green
        self.red = red
        self.items = items
        self.place(x=0, y=0, width=800, height=700)

        tk.Label(self, text="Моя кладовая", font=TITLE_FONT, bg='white').pack(pady=20)

        # Таблица
        columns = ('Продукт', 'Количество')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=10)
        self.tree.heading('Продукт', text='Продукт')
        self.tree.heading('Количество', text='Количество')
        self.tree.column('Продукт', width=300)
        self.tree.column('Количество', width=200)
        self.tree.pack(pady=20, padx=20, fill='both', expand=True)

        self.update_table()

        # Кнопки изменения/удаления (большие, рядом)
        btn_frame = tk.Frame(self, bg='white')
        btn_frame.pack(pady=10)
        self.change_btn = ttk.Button(btn_frame, text='Изменить', width=15, command=self.change_item)
        self.change_btn.pack(side='left', padx=10)
        self.delete_btn = ttk.Button(btn_frame, text='Удалить', width=15, command=self.delete_item)
        self.delete_btn.pack(side='left', padx=10)

        # Добавление (input без bg)
        add_frame = tk.Frame(self, bg='white')
        add_frame.pack(pady=10)
        tk.Label(add_frame, text="Название:", font=BODY_FONT, bg='white').pack(side='left')
        self.p_name = tk.Entry(add_frame, width=15, font=BODY_FONT, relief='flat', bd=0, bg='white')
        self.p_name.pack(side='left', padx=5)
        tk.Label(add_frame, text="Количество:", font=BODY_FONT, bg='white').pack(side='left', padx=5)
        self.p_amount = tk.Entry(add_frame, width=10, font=BODY_FONT, relief='flat', bd=0, bg='white')
        self.p_amount.pack(side='left', padx=5)
        ttk.Button(add_frame, text="Добавить", command=self.add_item).pack(side='left', padx=10)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.items:
            self.tree.insert('', 'end', values=(item['name'], item['amount']))

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