import tkinter as tk
from tkinter import ttk, messagebox
import json
from config import GREEN, RED, GRAY, PANTRY_ITEMS, SHOPPING_ITEMS, FAVORITES, TITLE_FONT, HEADER_FONT, BODY_FONT, \
    SMALL_FONT
from db import Database
from recipe_utils import (
    filter_favorites_by_query,
    merge_missing_into_shopping,
    parse_ingredients_string,
    missing_ingredients_vs_pantry,
)
from mealdb_api import lookup_meal, search_by_ingredient, search_by_name
from screens.main_screen import MainScreen
from screens.pantry_screen import PantryScreen
from screens.recipes_screen import RecipesScreen
from screens.shopping_screen import ShoppingScreen
from screens.favorites_screen import FavoritesScreen
from screens.add_recipe_screen import AddRecipeScreen
from screens.login_screen import LoginScreen


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

        self.current_tab = 'login'
        self.authenticated = False

        self.frames = {}
        self.create_screens()
        self.create_bottom_nav()
        self.nav_frame.pack_forget()
        self.show_frame('login')

    def handle_registration(self, username, password):
        """Метод для обработки регистрации из интерфейса"""
        if not username or not password:
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return

        # Вызов 'серверной' логики из db.py
        success = self.db.register_user(username, password)
        
        if success:
            messagebox.showinfo("Успех", f"Аккаунт {username} создан!")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить пользователя.")

    def handle_login(self, username, password):
        """Метод для обработки входа из интерфейса"""
        if not username or not password:
            messagebox.showwarning("Ошибка", "Введите логин и пароль!")
            return

        # Вызов серверной логики из db.py
        is_valid = self.db.authenticate_user(username, password)
        
        if is_valid:
            messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
            self.authenticated = True
            self.nav_frame.pack(side='bottom', fill='x')
            self.show_frame('main')
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")

    def create_screens(self):
        self.frames['main'] = MainScreen(self.root, self, self.green)
        self.frames['pantry'] = PantryScreen(self.root, self, self.green, self.red, self.pantry_items)
        self.frames['recipes'] = RecipesScreen(self.root, self, self.green, self)
        self.frames['shopping'] = ShoppingScreen(self.root, self, self.green, self.red, self.shopping_items)
        self.frames['favorites'] = FavoritesScreen(self.root, self, self.green, self.gray, self.favorites)
        self.frames['add'] = AddRecipeScreen(self.root, self, self.green, self.gray, self)
        self.frames['login'] = LoginScreen(self.root, self, self.green)

    def create_bottom_nav(self):
        # Делаем панель выше и светлее
        self.nav_frame = tk.Frame(self.root, bg="#F8F9FA", height=120, bd=1, relief='sunken')
        self.nav_frame.pack(side='bottom', fill='x')

        buttons = [
            ('main', '🏠 Главная'),
            ('favorites', '⭐ Избранное'),
            ('add', '➕ Свой рецепт'),
            ('shopping', '🛒 Покупки')
        ]
        
        for i, (tab, text) in enumerate(buttons):
            btn = ttk.Button(self.nav_frame, text=text, command=lambda t=tab: self.show_frame(t))
            btn.grid(row=0, column=i, sticky='ew', padx=10, pady=25) # Больше отступов

    def show_frame(self, frame_name):
        if not self.authenticated and frame_name != 'login':
            messagebox.showwarning("Требуется вход", "Войдите в аккаунт, чтобы пользоваться приложением.")
            return
        for frame in self.frames.values():
            frame.place_forget()
        self.frames[frame_name].place(x=0, y=0, width=800, height=700)
        self.current_tab = frame_name
        self.update_tab_highlight()
        self.animate_fade_in(self.frames[frame_name])

        if frame_name == 'pantry':
            self.frames['pantry'].update_table()
        if frame_name == 'favorites':
            self.frames['favorites'].update_grid()
        if frame_name == 'shopping':
            self.frames['shopping'].update_checkboxes()

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
        if not self.authenticated:
            messagebox.showwarning("Требуется вход", "Войдите в аккаунт, чтобы искать рецепты.")
            return
        if not query:
            messagebox.showwarning("Ошибка", "Введите название или ингредиент!")
            return

        # 1. ПОИСК В ЛОКАЛЬНОЙ БАЗЕ
        # Фильтруем те, что ты добавил вручную
        local_results = filter_favorites_by_query(self.favorites, query)
        
        if local_results:
            self.recipes_data = []
            for r in local_results:
                self.recipes_data.append({
                    'name': r['name'], # Унифицируем: всегда используем 'name'
                    'ingredients': r.get('ingredients', ''),
                    'instructions': r.get('instructions', 'Инструкция не найдена'),
                    'local': True  
                })
            self.show_frame('recipes')
            self.frames['recipes'].update_list()
            return 

        # 2. ПОИСК В ИНТЕРНЕТЕ (TheMealDB)
        try:
            translator = {
                'помидоры': 'tomato',
                'сыр': 'cheese',
                'курица': 'chicken',
                'рис': 'rice',
                'яйца': 'egg',
                'мясо': 'beef',
                'паста': 'pasta',
                'лук': 'onion',
                'чеснок': 'garlic',
            }
            token = query.split(',')[0].strip().lower()
            eng_ing = translator.get(token, token)

            self.recipes_data = search_by_ingredient(eng_ing)
            if not self.recipes_data:
                self.recipes_data = search_by_name(query.strip())

            if not self.recipes_data:
                messagebox.showinfo("Результат", f"Рецепты по запросу «{query}» не найдены.")
                return

            self.show_frame('recipes')
            self.frames['recipes'].update_list()

        except Exception as e:
            messagebox.showerror("Ошибка поиска", f"Ошибка сети: {e}")

    def add_to_favorites(self, recipe):
        if not self.authenticated:
            messagebox.showwarning("Требуется вход", "Войдите в аккаунт.")
            return
        r = dict(recipe)
        mid = r.get('id') or r.get('meal_id')
        if mid:
            mid = str(mid)
            loaded = lookup_meal(mid)
            if loaded:
                r.update(loaded)

        row = {
            'name': (r.get('name') or 'Без названия').strip(),
            'ingredients': (r.get('ingredients') or '').strip(),
            'instructions': (r.get('instructions') or '').strip(),
            'time': (r.get('time') or '—'),
            'meal_id': mid if mid else None,
            'local': bool(r.get('local', False)) if mid else True,
        }

        if row['meal_id']:
            if any((f.get('meal_id') or '') == row['meal_id'] for f in self.favorites):
                messagebox.showinfo("Избранное", "Этот рецепт уже в избранном.")
                return
        else:
            name_key = row['name'].lower()
            if any((f.get('name') or '').strip().lower() == name_key for f in self.favorites):
                messagebox.showinfo("Избранное", "Рецепт с таким названием уже в избранном.")
                return

        self.favorites.append(row)
        self.db.save_favorites(self.favorites)
        self.frames['favorites'].update_grid()

    def remove_from_favorites(self, index):
        if 0 <= index < len(self.favorites):
            del self.favorites[index]
            self.db.save_favorites(self.favorites)
            self.frames['favorites'].update_grid()

    def add_missing_to_shopping(self, missing_ings):
        self.shopping_items = merge_missing_into_shopping(self.shopping_items, missing_ings)
        self.db.save_shopping(self.shopping_items)
        self.frames['shopping'].update_checkboxes()

    def add_missing_from_recipe(self, recipe) -> int:
        """Добавляет недостающие ингредиенты рецепта в кладовую с количеством 0. Возвращает число новых позиций."""
        r = dict(recipe)
        full = r.get('full_ingredients') or []
        rid = r.get('id') or r.get('meal_id')
        if not full and rid and not r.get('local'):
            data = lookup_meal(str(rid))
            if data:
                full = data.get('full_ingredients') or []
        if not full and r.get('ingredients'):
            full = parse_ingredients_string(r['ingredients'])
        missing = missing_ingredients_vs_pantry(full, self.pantry_items)
        if missing:
            for ing in missing:
                self.pantry_items.append({'name': ing['name'], 'amount': '0'})
            self.update_pantry_items(self.pantry_items)
            self.frames['pantry'].update_table()
        return len(missing)

    def show_recipe_details(self, recipe, from_source='favorites'):
        if not self.authenticated:
            messagebox.showwarning("Требуется вход", "Войдите в аккаунт.")
            return
        recipe = dict(recipe)
        rid = recipe.get('id') or recipe.get('meal_id')

        # Lazy load из TheMealDB по id
        if rid and not recipe.get('local'):
            need = not (recipe.get('instructions') or '').strip() or not (recipe.get('ingredients') or '').strip()
            if need:
                loaded = lookup_meal(str(rid))
                if loaded:
                    recipe.update(loaded)
                elif not recipe.get('instructions'):
                    recipe['instructions'] = 'Не удалось загрузить рецепт по сети.'

        # --- ШАГ 2: СОЗДАНИЕ ИНТЕРФЕЙСА ОКНА ---
        detail_window = tk.Toplevel(self.root)
        # Учитываем, что в разных источниках может быть 'name' или 'title'
        recipe_name = recipe.get('name') or recipe.get('title') or "Без названия"
        
        detail_window.title(f"Рецепт: {recipe_name}")
        detail_window.geometry("600x700")
        detail_window.configure(bg='white')

        # Красивый заголовок
        header_frame = tk.Frame(detail_window, bg=self.green, height=80)
        header_frame.pack(fill='x')
        tk.Label(header_frame, text=recipe_name.upper(), font=TITLE_FONT, fg='white', bg=self.green).pack(pady=20)

        # Контейнер со скроллом
        canvas_frame = tk.Frame(detail_window, bg='white')
        canvas_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
        scrollable_content = tk.Frame(canvas, bg='white')

        scrollable_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_content, anchor='nw', width=520)
        canvas.configure(yscrollcommand=scrollbar.set)

        # --- ШАГ 3: ОТОБРАЖЕНИЕ ИНГРЕДИЕНТОВ ---
        tk.Label(scrollable_content, text="🛒 ИНГРЕДИЕНТЫ", font=HEADER_FONT, bg='white', fg=self.green).pack(anchor='w', pady=(0, 10))
        
        # Получаем список ингредиентов (предпочитаем full_ingredients для точной проверки)
        full_ings = recipe.get('full_ingredients') or []
        if not full_ings and recipe.get('ingredients'):
            full_ings = parse_ingredients_string(recipe['ingredients'])
        
        if full_ings:
            for ing in full_ings:
                name = ing.get('name', '').strip()
                amount = ing.get('amount', '').strip()
                display_text = f"{name} ({amount})" if amount else name
                
                # Проверяем наличие в кладовой
                in_pantry = any(p['name'].lower() == name.lower() for p in self.pantry_items)
                color = self.green if in_pantry else self.red
                
                f = tk.Frame(scrollable_content, bg="#F1F8E9", pady=2)
                f.pack(fill='x', pady=2)
                tk.Label(f, text=f"  • {display_text}", font=BODY_FONT, bg="#F1F8E9", fg=color).pack(side='left')
        else:
            tk.Label(scrollable_content, text="Список ингредиентов пуст", font=BODY_FONT, bg='white', fg='gray').pack(anchor='w')

        # --- ШАГ 4: ОТОБРАЖЕНИЕ ИНСТРУКЦИИ ---
        tk.Label(scrollable_content, text="👨‍🍳 ИНСТРУКЦИЯ ПО ПРИГОТОВЛЕНИЮ", font=HEADER_FONT, bg='white', fg=self.green).pack(anchor='w', pady=(25, 10))
        
        # Берем текст инструкции и делаем его читаемым (добавляем абзацы)
        raw_text = recipe.get('instructions', 'Инструкция не предоставлена.')
        nice_text = raw_text.replace('. ', '.\n\n')
        
        instructions_label = tk.Label(scrollable_content, text=nice_text, font=BODY_FONT, bg='white', 
                                      justify='left', wraplength=500, fg="#444")
        instructions_label.pack(anchor='w', pady=5)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Панель кнопок внизу (Footer)
        footer = tk.Frame(detail_window, bg='#F5F5F5', pady=15)
        footer.pack(fill='x', side='bottom')

        if from_source == 'search':
            ttk.Button(footer, text="В избранное", command=lambda: self.add_to_favorites(recipe)).pack(
                side='left', padx=20
            )

        def add_missing_cb():
            n = self.add_missing_from_recipe(recipe)
            if n:
                messagebox.showinfo("Кладовая", f"Добавлено в кладовую: {n}.")
            else:
                messagebox.showinfo(
                    "OK",
                    "Все ингредиенты уже есть в кладовой или не удалось разобрать список ингредиентов.",
                )

        ttk.Button(
            footer,
            text="Добавить недостающие в кладовую",
            command=add_missing_cb,
        ).pack(side='left', padx=20)

        ttk.Button(footer, text="Закрыть", command=detail_window.destroy).pack(side='right', padx=20)
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