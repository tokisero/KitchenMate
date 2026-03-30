import tkinter as tk
from config import HEADER_FONT, SMALL_FONT, GREEN
from tkinter import ttk, messagebox
import webbrowser
from config import TITLE_FONT, HEADER_FONT, BODY_FONT, GREEN


class RecipesScreen(tk.Frame):
    def __init__(self, parent, controller, green, app):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.app = app
        self.green = green
        self.red = app.red  # Фикс: red из app
        self.gray = app.gray  # Фикс: gray из app
        self.recipes_data = []
        self.place(x=0, y=0, width=800, height=700)

        tk.Label(self, text="Найденные рецепты", font=TITLE_FONT, bg='white').pack(pady=30)

        # Scrollable для карточек (полный вид)
        canvas_frame = tk.Frame(self, bg='white')
        canvas_frame.pack(fill='both', expand=True, padx=30, pady=20)
        self.canvas = tk.Canvas(canvas_frame, bg='white', height=500)
        scrollbar = tk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        self.scrollable_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Скролл колёсиком
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Кнопка
        ttk.Button(self, text="Сохранить отсутствующие в список покупок", command=self.save_missing_to_shopping).pack(
            pady=20)

    def update_list(self):
        # Очистка старого списка
        for child in self.scrollable_frame.winfo_children():
            child.destroy()

        if not self.controller.recipes_data:
            tk.Label(self.scrollable_frame, text="Ничего не найдено", font=HEADER_FONT, bg='white').pack(pady=20)
            return

        for recipe in self.controller.recipes_data:
            display_name = recipe.get('name') or recipe.get('title') or "Без названия"
            
            # Создаем карточку
            card = tk.Frame(self.scrollable_frame, bg='white', highlightbackground="#2D5A27", 
                            highlightthickness=1, padx=15, pady=15)
            card.pack(fill='x', pady=10, padx=10)

            # Название рецепта
            tk.Label(card, text=display_name, font=HEADER_FONT, bg='white', 
                     fg="#2D5A27", wraplength=500, justify='left').pack(anchor='w', pady=(0, 5))

            # Ингредиенты (кратко)
            ings_text = recipe.get('ingredients', '')
            if ings_text:
                tk.Label(card, text=f"Ингредиенты: {ings_text[:100]}...", 
                         font=SMALL_FONT, bg='white', fg='gray').pack(anchor='w')

            # Кнопка открытия
            btn_frame = tk.Frame(card, bg='white')
            btn_frame.pack(fill='x', pady=(10, 0))
            
            ttk.Button(btn_frame, text="📖 Инструкция", 
                       command=lambda r=recipe: self.controller.show_recipe_details(r, from_source='search' if not r.get('local') else 'favorites')).pack(side='left') 
            
        def add_to_favorite(self, recipe):
            favorite_recipe = {
            'name': recipe['title'],
            'ingredients': ', '.join(
                [f"{i['amount']} {i['name'].title()}" for i in recipe.get('full_ingredients', [])]),
            'instructions': 'Инструкции на сайте',
            'time': '30 мин'
        }
        self.app.add_to_favorites(favorite_recipe)
        messagebox.showinfo("Добавлено", f"{recipe['title']} сохранён в избранное!")

    def save_missing_to_shopping(self):
        missing_all = []
        for recipe in self.app.recipes_data:
            for ing in recipe.get('full_ingredients', []):
                name = ing['name'].lower()
                if not any(p['name'].lower() == name for p in self.app.pantry_items):
                    if ing not in missing_all:
                        missing_all.append(ing)

        if missing_all:
            self.app.add_missing_to_shopping(missing_all)
            messagebox.showinfo("Добавлено", f"Добавлено {len(missing_all)} ингредиентов в список покупок!")
        else:
            messagebox.showinfo("OK", "Все ингредиенты есть в кладовой!")