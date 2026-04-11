import tkinter as tk
from tkinter import ttk, messagebox
from config import TITLE_FONT, HEADER_FONT, BODY_FONT, SMALL_FONT


class RecipesScreen(tk.Frame):
    def __init__(self, parent, controller, green, app):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.app = app
        self.green = green
        self.red = app.red
        self.gray = app.gray
        self.recipes_data = []
        self.place(x=0, y=0, width=800, height=700)

        tk.Label(self, text="Найденные рецепты", font=TITLE_FONT, bg='white').pack(pady=30)

        canvas_frame = tk.Frame(self, bg='white')
        canvas_frame.pack(fill='both', expand=True, padx=30, pady=20)
        self.canvas = tk.Canvas(canvas_frame, bg='white', height=500)
        scrollbar = tk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        self.scrollable_frame.bind(
            '<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        ttk.Button(
            self,
            text="Добавить отсутствующие в кладовую",
            command=self.add_missing_to_pantry,
        ).pack(pady=20)

    def update_list(self):
        for child in self.scrollable_frame.winfo_children():
            child.destroy()

        if not self.controller.recipes_data:
            tk.Label(self.scrollable_frame, text="Ничего не найдено", font=HEADER_FONT, bg='white').pack(pady=20)
            return

        for recipe in self.controller.recipes_data:
            display_name = recipe.get('name') or recipe.get('title') or "Без названия"

            card = tk.Frame(
                self.scrollable_frame,
                bg='white',
                highlightbackground="#2D5A27",
                highlightthickness=1,
                padx=15,
                pady=15,
            )
            card.pack(fill='x', pady=10, padx=10)

            tk.Label(
                card,
                text=display_name,
                font=HEADER_FONT,
                bg='white',
                fg="#2D5A27",
                wraplength=500,
                justify='left',
            ).pack(anchor='w', pady=(0, 5))

            ings_text = recipe.get('ingredients', '')
            if ings_text:
                tk.Label(
                    card,
                    text=f"Ингредиенты: {ings_text[:100]}...",
                    font=SMALL_FONT,
                    bg='white',
                    fg='gray',
                ).pack(anchor='w')

            btn_frame = tk.Frame(card, bg='white')
            btn_frame.pack(fill='x', pady=(10, 0))

            src = 'search' if not recipe.get('local') else 'favorites'
            ttk.Button(
                btn_frame,
                text="Открыть инструкцию",
                command=lambda r=recipe, s=src: self.controller.show_recipe_details(r, from_source=s),
            ).pack(side='left')

    def add_missing_to_pantry(self):
        if not self.app.authenticated:
            messagebox.showwarning("Требуется вход", "Войдите в аккаунт.")
            return
        from mealdb_api import lookup_meal

        missing_all = []
        seen_names = set()

        for recipe in self.app.recipes_data:
            full = recipe.get('full_ingredients') or []
            if not full and recipe.get('id'):
                data = lookup_meal(str(recipe['id']))
                if data:
                    full = data.get('full_ingredients') or []

            if not full:
                continue

            for ing in full:
                name = ing.get('name', '').strip()
                if not name:
                    continue
                key = name.lower()
                if key in seen_names:
                    continue
                if not any(p['name'].lower() == key for p in self.app.pantry_items):
                    missing_all.append(
                        {'name': ing['name'], 'amount': '0'}
                    )
                    seen_names.add(key)

        if missing_all:
            self.app.pantry_items.extend(missing_all)
            self.app.update_pantry_items(self.app.pantry_items)
            self.app.frames['pantry'].update_table()
            messagebox.showinfo("Кладовая", f"Добавлено в кладовую: {len(missing_all)}.")
        else:
            messagebox.showinfo(
                "OK",
                "Нет отсутствующих ингредиентов по открытым рецептам (или всё уже в кладовой).",
            )
