import tkinter as tk


class MainScreen(tk.Frame):
    def __init__(self, parent, controller, green):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.place(x=0, y=0, width=400, height=600)

        tk.Label(self, text="KitchenMate", font=('Arial', 24, 'bold'), bg='white').pack(pady=50)

        self.search_entry = tk.Entry(self, font=('Arial', 14), width=30, justify='center')
        self.search_entry.pack(pady=20)

        tk.Button(self, text="Найти рецепты", bg=green, fg='white', font=('Arial', 12), width=20,
                  command=lambda: self.controller.search_recipes(self.search_entry.get())).pack(pady=10)

        tk.Button(self, text="Моя кладовая", bg=green, fg='white', font=('Arial', 12), width=20,
                  command=lambda: self.controller.show_frame('pantry')).pack(pady=10)