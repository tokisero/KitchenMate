import tkinter as tk
from tkinter import messagebox
import webbrowser
from config import TITLE_FONT, HEADER_FONT, BODY_FONT, GREEN


class RecipesScreen(tk.Frame):
    def __init__(self, parent, controller, green, app):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.app = app
        self.green = green
        self.recipes_data = []
        self.place(x=0, y=0, width=800, height=700)

        tk.Label(self, text="Найденные рецепты", font=TITLE_FONT, bg='white').pack(pady=20)

        # Scrollable для карточек
        canvas_frame = tk.Frame(self, bg='white')
        canvas_frame.pack(fill='both', expand=True, padx=20, pady=10)
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
        tk.Button(self, text="Сохранить отсутствующие в список покупок", bg=self.green, fg='white', font=BODY_FONT,
                  command=self.save_missing_to_shopping).pack(pady=5)

    def update_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for recipe in self.app.recipes_data:
            card = tk.Frame(self.scrollable_frame, bg='white', relief='solid', bd=1, padx=10, pady=10)
            card.pack(fill='x', pady=5)

            # Название
            tk.Label(card, text=recipe['title'], font=HEADER_FONT, bg='white').pack(anchor='w')

            # Ингредиенты с цветом
            ing_frame = tk.Frame(card, bg='white')
            ing_frame.pack(fill='x', pady=5)
            for ing in recipe.get('full_ingredients', []):
                name = ing['name'].lower()
                pantry_match = any(p['name'].lower() == name for p in self.app.pantry_items)
                color = self.green if pantry_match else self.red
                fg = 'white' if color == self.red else 'black'
                bg = 'lightgreen' if pantry_match else 'lightcoral'
                label = tk.Label(ing_frame, text=f"{ing['amount']} {ing['name'].title()}", fg=fg, bg=bg, font=BODY_FONT,
                                 relief='solid', bd=1, padx=5)
                label.pack(anchor='w', pady=1)

            # Сердечко
            heart = tk.Label(card, text='♥', font=('Arial', 20), fg=self.green, bg='white')
            heart.pack(anchor='e')
            heart.bind('<Button-1>', lambda e, r=recipe: self.add_to_favorite(r))

            # Клик по карточке — детали
            card.bind('<Button-1>', lambda e, r=recipe: self.app.show_recipe_details(r, 'search'))

        self.canvas.update_idletasks()
        print(f"Debug UI: Добавлено {len(self.app.recipes_data)} карточек")

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