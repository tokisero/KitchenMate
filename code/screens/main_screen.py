import tkinter as tk
from tkinter import ttk  # Фикс: импорт ttk
from config import TITLE_FONT, BODY_FONT


class MainScreen(tk.Frame):
    def __init__(self, parent, controller, green):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.place(x=0, y=0, width=800, height=700)

        # Центрирование
        main_container = tk.Frame(self, bg='white')
        main_container.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(main_container, text="KitchenMate", font=TITLE_FONT, bg='white').pack(pady=50)

        self.search_entry = tk.Entry(main_container, font=BODY_FONT, width=40)
        self.search_entry.pack(pady=20)

        ttk.Button(main_container, text="Найти рецепты",
                   command=lambda: self.controller.search_recipes(self.search_entry.get())).pack(pady=10)

        ttk.Button(main_container, text="Моя кладовая", command=lambda: self.controller.show_frame('pantry')).pack(
            pady=10)