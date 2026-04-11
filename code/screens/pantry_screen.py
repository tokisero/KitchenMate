import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from config import TITLE_FONT, BODY_FONT, SOFT_GREEN
from ui_helpers import confirm_destructive


class PantryScreen(tk.Frame):
    def __init__(self, parent, controller, green, red, items):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.green = green
        self.red = red
        self.items = items
        self.place(x=0, y=0, width=800, height=700)

        tk.Label(self, text="Моя кладовая", font=TITLE_FONT, bg='white').pack(pady=20)

        self.list_area = tk.Frame(self, bg='white')
        self.list_area.pack(pady=10, padx=20, fill='both', expand=True)

        # Таблица
        columns = ('Продукт', 'Количество')
        self.tree = ttk.Treeview(self.list_area, columns=columns, show='headings', height=10)
        self.tree.heading('Продукт', text='Продукт')
        self.tree.heading('Количество', text='Количество')
        self.tree.column('Продукт', width=300)
        self.tree.column('Количество', width=200)

        # Empty state (onboarding)
        self.empty_state = tk.Frame(
            self.list_area,
            bg=SOFT_GREEN,
            highlightbackground=self.green,
            highlightthickness=2,
            padx=24,
            pady=32,
        )
        tk.Label(
            self.empty_state,
            text="Пока нет продуктов",
            font=TITLE_FONT,
            bg=SOFT_GREEN,
            fg=self.green,
        ).pack(anchor='w')
        tk.Label(
            self.empty_state,
            text="Добавьте первый продукт в форме ниже: укажите название и количество,\nзатем нажмите «Добавить».",
            font=BODY_FONT,
            bg=SOFT_GREEN,
            justify='left',
        ).pack(anchor='w', pady=(12, 0))

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

        self.p_name.bind("<Return>", lambda e: self.p_amount.focus_set())
        self.p_amount.bind("<Return>", self.add_item)
        self.p_name.bind("<Escape>", lambda e: self.p_name.delete(0, tk.END))
        self.p_amount.bind("<Escape>", lambda e: self.p_amount.delete(0, tk.END))

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if not self.items:
            self.tree.pack_forget()
            self.empty_state.pack(fill='both', expand=True)
        else:
            self.empty_state.pack_forget()
            self.tree.pack(fill='both', expand=True)
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
        name = self.items[idx]['name']
        if confirm_destructive(
            self,
            "Удаление продукта",
            f"Удалить «{name}» из кладовой?",
            "Это действие нельзя отменить.",
        ):
            del self.items[idx]
            self.controller.update_pantry_items(self.items)
            self.update_table()