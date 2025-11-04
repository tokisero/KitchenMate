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

        # Scrollable
        canvas_frame = tk.Frame(self, bg='white')
        canvas_frame.pack(fill='both', expand=True, padx=20, pady=10)
        self.canvas = tk.Canvas(canvas_frame, bg='white', height=600)
        scrollbar = tk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        self.scrollable_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.create_forms()

    def create_forms(self):
        tk.Label(self.scrollable_frame, text="Добавить свой рецепт", font=TITLE_FONT, bg='white').pack(pady=20)

        tk.Label(self.scrollable_frame, text="Название рецепта:", font=BODY_FONT, bg='white').pack()
        self.name_entry = tk.Entry(self.scrollable_frame, width=50, font=BODY_FONT)
        self.name_entry.pack(pady=10)

        # Ингредиент (combo + кнопка)
        ing_frame = tk.Frame(self.scrollable_frame, bg='white')
        ing_frame.pack(pady=10)
        tk.Label(ing_frame, text="Ингредиент:", font=BODY_FONT, bg='white').pack(side='left')
        self.ing_combo = ttk.Combobox(ing_frame, values=INGREDIENTS_OPTIONS, width=30, font=BODY_FONT)
        self.ing_combo.pack(side='left', padx=10)
        tk.Button(ing_frame, text="Добавить", bg=self.green, fg='white', font=BODY_FONT, width=15,
                  command=self.add_ingredient).pack(side='left', padx=10)

        # Listbox для ингредиентов
        tk.Label(self.scrollable_frame, text="Список ингредиентов:", font=BODY_FONT, bg='white').pack(pady=(10, 0))
        self.ing_listbox = tk.Listbox(self.scrollable_frame, height=6, width=60, font=BODY_FONT)
        self.ing_listbox.pack(pady=10)

        # Инструкция
        tk.Label(self.scrollable_frame, text="Инструкция:", font=BODY_FONT, bg='white').pack()
        self.instr_text = tk.Text(self.scrollable_frame, height=6, width=60, font=BODY_FONT)
        self.instr_text.pack(pady=10)

        # Время
        tk.Label(self.scrollable_frame, text="Время приготовления:", font=BODY_FONT, bg='white').pack()
        self.time_combo = ttk.Combobox(self.scrollable_frame, values=TIME_OPTIONS, width=57, font=BODY_FONT)
        self.time_combo.pack(pady=10)

        # Кнопки
        tk.Button(self.scrollable_frame, text="Сохранить рецепт", bg=self.green, fg='white', font=BODY_FONT, width=25,
                  command=self.save_recipe).pack(pady=20)
        tk.Button(self.scrollable_frame, text="Назад", bg=self.gray, fg='white', font=BODY_FONT, width=25,
                  command=lambda: self.controller.show_frame('main')).pack()

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