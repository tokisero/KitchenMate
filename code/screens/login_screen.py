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

        def do_login(_event=None):
            controller.handle_login(self.username_entry.get(), self.password_entry.get())

        def do_register(_event=None):
            controller.handle_registration(self.username_entry.get(), self.password_entry.get())

        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", do_login)
        self.username_entry.bind("<Escape>", lambda e: self.username_entry.delete(0, tk.END))
        self.password_entry.bind("<Escape>", lambda e: self.password_entry.delete(0, tk.END))

        # Кнопки
        btn_frame = tk.Frame(self, bg='white')
        btn_frame.pack(pady=30)

        ttk.Button(btn_frame, text="Войти", width=15, command=do_login).pack(side='left', padx=10)

        ttk.Button(btn_frame, text="Регистрация", width=15, command=do_register).pack(side='left', padx=10)

        self.after(100, lambda: self.username_entry.focus_set())