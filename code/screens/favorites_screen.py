import tkinter as tk
from tkinter import ttk
from config import TITLE_FONT, HEADER_FONT, BODY_FONT, SOFT_GREEN
from ui_helpers import confirm_destructive


class FavoritesScreen(tk.Frame):
    def __init__(self, parent, controller, green, gray, favorites):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.green = green
        self.gray = gray
        self.favorites = favorites
        self.place(x=0, y=0, width=800, height=700)

        tk.Label(self, text="Избранные рецепты", font=TITLE_FONT, bg='white').pack(pady=20)

        # Scrollable grid
        canvas_frame = tk.Frame(self, bg='white')
        canvas_frame.pack(fill='both', expand=True, padx=20, pady=10)
        self.canvas = tk.Canvas(canvas_frame, bg='white', height=400)
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

        self.update_grid()

    def update_grid(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.favorites:
            self.empty_state = tk.Frame(
                self.scrollable_frame,
                bg=SOFT_GREEN,
                highlightbackground=self.green,
                highlightthickness=2,
                padx=24,
                pady=40,
            )
            self.empty_state.pack(fill='both', expand=True, padx=40, pady=40)
            tk.Label(
                self.empty_state,
                text="Нет избранных рецептов",
                font=TITLE_FONT,
                bg=SOFT_GREEN,
                fg=self.green,
            ).pack(anchor='w')
            tk.Label(
                self.empty_state,
                text="Найдите рецепт на вкладке поиска и добавьте его в избранное из карточки рецепта.",
                font=BODY_FONT,
                bg=SOFT_GREEN,
                justify='left',
                wraplength=480,
            ).pack(anchor='w', pady=(12, 0))
            return

        for idx, recipe in enumerate(self.favorites):
            row = idx // 2
            col = idx % 2
            card = tk.Frame(self.scrollable_frame, bg='white', relief='flat', bd=0, padx=20, pady=20)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

            photo = tk.Canvas(card, width=100, height=100, bg=self.gray, relief='flat')
            photo.pack(pady=5)

            tk.Label(card, text=recipe['name'], font=HEADER_FONT, bg='white').pack(pady=5)

            ttk.Button(
                card,
                text="Открыть рецепт",
                width=22,
                command=lambda r=recipe: self.controller.show_recipe_details(r, 'favorites'),
            ).pack(pady=4)

            ttk.Button(
                card,
                text="Удалить из избранного",
                width=22,
                command=lambda i=idx: self.remove_recipe(i),
            ).pack(pady=4)

    def remove_recipe(self, idx):
        name = self.favorites[idx]['name']
        if confirm_destructive(
            self,
            "Удаление из избранного",
            f"Убрать «{name}» из избранного?",
            "Рецепт можно будет добавить снова через поиск.",
        ):
            self.controller.remove_from_favorites(idx)