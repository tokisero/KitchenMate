import tkinter as tk
from tkinter import ttk

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller, green):
        super().__init__(parent, bg='white')
        self.controller = controller

        tk.Label(self, text="Вход в KitchenMate", font=("Arial", 24, "bold"), bg='white').pack(pady=50)

        # Поля ввода
        tk.Label(self, text="Логин:", bg='white', font=("Arial", 12)).pack()
        self.username_entry = ttk.Entry(self, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Пароль:", bg='white', font=("Arial", 12)).pack()
        self.password_entry = ttk.Entry(self, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Кнопки
        btn_frame = tk.Frame(self, bg='white')
        btn_frame.pack(pady=30)

        ttk.Button(btn_frame, text="Войти", width=15, 
                   command=lambda: controller.handle_login(self.username_entry.get(), self.password_entry.get())).pack(side='left', padx=10)
        
        ttk.Button(btn_frame, text="Регистрация", width=15, 
                   command=lambda: controller.handle_registration(self.username_entry.get(), self.password_entry.get())).pack(side='left', padx=10)