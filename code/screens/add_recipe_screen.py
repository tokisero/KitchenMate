import tkinter as tk
from tkinter import ttk, messagebox
from config import TITLE_FONT, BODY_FONT, INGREDIENTS_OPTIONS, TIME_OPTIONS, GREEN, GRAY


class AddRecipeScreen(tk.Frame):
    def __init__(self, parent, controller, green, gray, app):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.app = app
        self.green = green
        self.gray = gray
        self.ingredients_list = []
        self.place(x=0, y=0, width=800, height=700)

        self.create_forms()

    def create_forms(self):
        tk.Label(self, text="Добавить свой рецепт", font=TITLE_FONT, bg='white').pack(pady=20)

        # Название
        tk.Label(self, text="Название рецепта:", font=BODY_FONT, bg='white').pack(pady=5)
        self.name_entry = ttk.Entry(self, width=40, font=BODY_FONT)  # Компактнее
        self.name_entry.pack(pady=5)

        # Ингредиент
        ing_frame = tk.Frame(self, bg='white')
        ing_frame.pack(pady=10)
        tk.Label(ing_frame, text="Ингредиент:", font=BODY_FONT, bg='white').pack(side='left')
        self.ing_combo = ttk.Combobox(ing_frame, values=INGREDIENTS_OPTIONS, width=25, font=BODY_FONT)  # Компактнее
        self.ing_combo.pack(side='left', padx=10)
        ttk.Button(ing_frame, text="Добавить", command=self.add_ingredient).pack(side='left', padx=10)

        # Список ингредиентов
        tk.Label(self, text="Список ингредиентов:", font=BODY_FONT, bg='white').pack(pady=(10, 0))
        self.ing_listbox = tk.Listbox(self, height=3, width=50, font=BODY_FONT)  # Уменьшено
        self.ing_listbox.pack(pady=5)

        # Инструкция
        tk.Label(self, text="Инструкция:", font=BODY_FONT, bg='white').pack(pady=5)
        self.instr_text = tk.Text(self, height=3, width=50, font=BODY_FONT)  # Уменьшено
        self.instr_text.pack(pady=5)

        # Время
        tk.Label(self, text="Время приготовления:", font=BODY_FONT, bg='white').pack(pady=5)
        self.time_combo = ttk.Combobox(self, values=TIME_OPTIONS, width=47, font=BODY_FONT)  # Компактнее
        self.time_combo.pack(pady=5)

        # Кнопки
        btn_frame = tk.Frame(self, bg='white')
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Сохранить рецепт", width=20, command=self.save_recipe).pack(side='left', padx=10)
        ttk.Button(btn_frame, text="Назад", width=20, command=lambda: self.controller.show_frame('main')).pack(
            side='left', padx=10)

    def add_ingredient(self):
        ing = self.ing_combo.get()
        if ing:
            self.ingredients_list.append(ing)
            self.ing_listbox.insert(tk.END, ing)
            self.ing_combo.set('')

    def save_recipe(self):
        name = self.name_entry.get()
        ingredients = ', '.join(self.ingredients_list)
        instructions = self.instr_text.get("1.0", tk.END).strip()
        time = self.time_combo.get()

        if not all([name, ingredients, instructions, time]):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        recipe = {
            'name': name,
            'ingredients': ingredients,
            'instructions': instructions,
            'time': time
        }
        self.app.add_to_favorites(recipe)
        messagebox.showinfo("Сохранено", f"Рецепт '{name}' добавлен в избранное!")

        # Очистка
        self.name_entry.delete(0, tk.END)
        self.ingredients_list = []
        self.ing_listbox.delete(0, tk.END)
        self.instr_text.delete("1.0", tk.END)
        self.time_combo.set('')