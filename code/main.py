import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from config import GREEN, RED, GRAY, PANTRY_ITEMS, SHOPPING_ITEMS, FAVORITES, TITLE_FONT, HEADER_FONT, BODY_FONT, \
    SMALL_FONT
from db import Database
from screens.main_screen import MainScreen
from screens.pantry_screen import PantryScreen
from screens.recipes_screen import RecipesScreen
from screens.shopping_screen import ShoppingScreen
from screens.favorites_screen import FavoritesScreen
from screens.add_recipe_screen import AddRecipeScreen


class KitchenMateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KitchenMate")
        self.root.geometry("800x800")
        self.root.resizable(False, False)
        self.root.configure(bg='white')

        self.green = GREEN
        self.red = RED
        self.gray = GRAY

        # ttk Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', padding=(15, 10), relief='flat', background=self.green, foreground='white',
                        font=SMALL_FONT)
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TEntry', padding=5, relief='flat', borderwidth=1)
        style.map('TEntry', bordercolor=[('focus', self.green)])
        style.configure('TCombobox', padding=5, relief='flat', borderwidth=1)
        style.map('TCombobox', bordercolor=[('focus', self.green)])

        # БД
        self.db = Database()
        self.pantry_items = self.db.load_pantry() or PANTRY_ITEMS.copy()
        self.shopping_items = self.db.load_shopping() or SHOPPING_ITEMS.copy()
        self.favorites = self.db.load_favorites() or FAVORITES.copy()
        self.recipes_data = []

        self.current_tab = 'main'

        self.frames = {}
        self.create_screens()
        self.create_bottom_nav()
        self.show_frame('main')

    def create_screens(self):
        self.frames['main'] = MainScreen(self.root, self, self.green)
        self.frames['pantry'] = PantryScreen(self.root, self, self.green, self.red, self.pantry_items)
        self.frames['recipes'] = RecipesScreen(self.root, self, self.green, self)
        self.frames['shopping'] = ShoppingScreen(self.root, self, self.green, self.red, self.shopping_items)
        self.frames['favorites'] = FavoritesScreen(self.root, self, self.green, self.gray, self.favorites)
        self.frames['add'] = AddRecipeScreen(self.root, self, self.green, self.gray, self)

    def create_bottom_nav(self):
        self.nav_frame = tk.Frame(self.root, bg=self.green, height=100)
        self.nav_frame.pack(side='bottom', fill='x')

        buttons = [
            ('main', 'Главное меню'),
            ('favorites', 'Избранное'),
            ('add', 'Добавить рецепт'),
            ('shopping', 'Список покупок')
        ]
        for i, (tab, text) in enumerate(buttons):
            btn = ttk.Button(self.nav_frame, text=text, command=lambda t=tab: self.show_frame(t))
            btn.grid(row=0, column=i, sticky='ew', padx=2, pady=20, ipadx=30)

        for i in range(4):
            self.nav_frame.grid_columnconfigure(i, weight=1)

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.place_forget()
        self.frames[frame_name].place(x=0, y=0, width=800, height=700)
        self.current_tab = frame_name
        self.update_tab_highlight()
        self.animate_fade_in(self.frames[frame_name])

    def update_tab_highlight(self):
        for child in self.nav_frame.winfo_children():
            child.configure(style='TButton')

        if self.current_tab in ['main', 'favorites', 'add', 'shopping']:
            idx = ['main', 'favorites', 'add', 'shopping'].index(self.current_tab)
            btn = self.nav_frame.grid_slaves(row=0, column=idx)[0]
            btn.configure(style='TButton')
            highlight = tk.Frame(btn, bg='lightgreen', relief='flat')
            highlight.place(relx=0.05, rely=1.1, relwidth=0.9, relheight=0.2)

    def animate_fade_in(self, frame):
        alpha = 0.2

        def fade_step():
            nonlocal alpha
            alpha += 0.1
            if alpha < 1.0:
                frame.configure(bg=f'#{int(255 * alpha):02x}{int(255 * alpha):02x}{int(255 * alpha):02x}')
                frame.after(50, fade_step)
            else:
                frame.configure(bg='white')

        fade_step()

    def search_recipes(self, query):
        if not query:
            messagebox.showwarning("Ошибка", "Введите ингредиенты!")
            return

        try:
            translator = {
                'помидоры': 'tomato',
                'сыр': 'cheese',
                'рис': 'rice',
                'курица': 'chicken',
                'мука': 'flour',
                'молоко': 'milk',
                'огурцы': 'cucumber'
            }
            ingredient = query.split(',')[0].strip().lower()
            eng_ing = translator.get(ingredient, ingredient)

            url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={eng_ing}"
            response = requests.get(url, timeout=10)

            print(f"Debug: Запрос для '{eng_ing}' - Status: {response.status_code}")

            if not response.ok:
                raise Exception(f"Ошибка сервера: {response.status_code}")

            data = response.json()
            meals = data.get('meals', [])
            print(f"Debug: Количество meals: {len(meals)}")

            if not meals:
                messagebox.showinfo("Результат", f"Рецепты для '{eng_ing}' не найдены!")
                return

            self.recipes_data = []
            for meal in meals[:5]:
                detail_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal['idMeal']}"
                detail_resp = requests.get(detail_url, timeout=5)
                full_ingredients = []
                if detail_resp.ok:
                    detail_data = detail_resp.json()
                    if detail_data.get('meals') and detail_data['meals'][0]:
                        recipe = detail_data['meals'][0]
                        for i in range(1, 21):
                            ing = recipe.get(f'strIngredient{i}')
                            if ing and (ing := ing.strip()):
                                meas = recipe.get(f'strMeasure{i}', '').strip()
                                full_ingredients.append({'name': ing.lower(), 'amount': meas if meas else '1 unit'})

                self.recipes_data.append({
                    'title': meal.get('strMeal', 'Без названия'),
                    'full_ingredients': full_ingredients,
                    'href': f"https://www.themealdb.com/meal/{meal['idMeal']}-{meal['strMeal'].lower().replace(' ', '_')}"
                })

            print(f"Debug: Добавлено рецептов: {len(self.recipes_data)}")

            self.show_frame('recipes')
            self.frames['recipes'].update_list()
        except Exception as e:
            print(f"Debug: Ошибка: {e}")
            messagebox.showerror("Ошибка поиска", f"Проблема: {e}")

    def add_to_favorites(self, recipe):
        self.favorites.append(recipe)
        self.db.save_favorites(self.favorites)
        self.frames['favorites'].update_grid()

    def remove_from_favorites(self, index):
        if 0 <= index < len(self.favorites):
            del self.favorites[index]
            self.db.save_favorites(self.favorites)
            self.frames['favorites'].update_grid()

    def add_missing_to_shopping(self, missing_ings):
        for ing in missing_ings:
            if not any(p['name'].lower() == ing['name'] for p in self.shopping_items):
                self.shopping_items.append({'name': ing['name'], 'amount': ing['amount'], 'checked': False})
        self.db.save_shopping(self.shopping_items)
        self.frames['shopping'].update_checkboxes()

    def show_recipe_details(self, recipe, from_source='favorites'):
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Детали: {recipe['name']}")
        detail_window.geometry("600x500")  # Фикс: 500px, кнопки видны
        detail_window.configure(bg='white')
        detail_window.resizable(False, False)

        tk.Label(detail_window, text=recipe['name'], font=TITLE_FONT, bg='white').pack(pady=20)

        # Scrollable (меньше высота)
        canvas_frame = tk.Frame(detail_window, bg='white')
        canvas_frame.pack(fill='both', expand=True, padx=20, pady=10)
        canvas = tk.Canvas(canvas_frame, bg='white', height=250)  # Фикс: меньше, кнопки видны
        scrollbar = tk.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
        scrollable = tk.Frame(canvas, bg='white')
        scrollable.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Ингредиенты
        tk.Label(scrollable, text="Ингредиенты:", font=HEADER_FONT, bg='white').pack(anchor='w', pady=(0, 5))
        for ing in recipe.get('ingredients', '').split(', '):
            tk.Label(scrollable, text=f"• {ing}", font=BODY_FONT, bg='white', fg=GREEN).pack(anchor='w')

        # Инструкция
        tk.Label(scrollable, text="Инструкция:", font=HEADER_FONT, bg='white').pack(anchor='w', pady=(10, 0))
        instr_label = tk.Label(scrollable, text=recipe['instructions'], font=BODY_FONT, bg='white', justify='left',
                               wraplength=550)
        instr_label.pack(pady=5)

        # Кнопки (pady=20 для видимости)
        btn_frame = tk.Frame(detail_window, bg='white')
        btn_frame.pack(pady=20)

        if from_source == 'search':
            ttk.Button(btn_frame, text="В избранное", width=20, command=lambda: self.add_to_favorites(recipe)).pack(
                side='left', padx=10, pady=10)
        else:
            ttk.Button(btn_frame, text="В покупки", width=20,
                       command=lambda: self.add_missing_to_shopping(recipe)).pack(side='left', padx=10, pady=10)

        ttk.Button(btn_frame, text="Закрыть", width=20, command=detail_window.destroy).pack(side='left', padx=10,
                                                                                            pady=10)

    def get_pantry_items(self):
        return self.pantry_items

    def update_pantry_items(self, items):
        self.pantry_items = items
        self.db.save_pantry(self.pantry_items)

    def __del__(self):
        self.db.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = KitchenMateApp(root)
    root.mainloop()