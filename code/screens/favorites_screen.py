import tkinter as tk
from tkinter import messagebox
from config import TITLE_FONT, HEADER_FONT, GREEN


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
        self.canvas = tk.Canvas(canvas_frame, bg='white', height=500)
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

        for idx, recipe in enumerate(self.favorites):
            row = idx // 2
            col = idx % 2
            card = tk.Frame(self.scrollable_frame, bg='white', relief='solid', bd=1)
            card.grid(row=row, column=col, padx=10, pady=10)
            card.bind('<Button-1>', lambda e, r=recipe: self.controller.show_recipe_details(r,
                                                                                            'favorites'))  # Клик по карточке — детали

            # Плейсхолдер
            photo = tk.Canvas(card, width=100, height=100, bg=self.gray)
            photo.pack(pady=5)

            # Название
            name_label = tk.Label(card, text=recipe['name'], font=HEADER_FONT, bg='white')
            name_label.pack()

            # Сердечко
            heart = tk.Label(card, text='♥', font=('Arial', 20), fg=self.green, bg='white')
            heart.pack()
            heart.bind('<Button-1>', lambda e, i=idx: self.remove_recipe(i))

    def remove_recipe(self, idx):
        if messagebox.askyesno("Удалить", f"Удалить '{self.favorites[idx]['name']}' из избранного?"):
            self.controller.remove_from_favorites(idx)