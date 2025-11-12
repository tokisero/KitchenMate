import tkinter as tk
from tkinter import messagebox
from config import TITLE_FONT, BODY_FONT


class ShoppingScreen(tk.Frame):
    def __init__(self, parent, controller, green, red, items):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.green = green
        self.red = red
        self.items = items
        self.shopping_vars = []
        self.check_frames = []
        self.place(x=0, y=0, width=800, height=700)

        tk.Label(self, text="Список покупок", font=TITLE_FONT, bg='white').pack(pady=20)

        # Scrollable (центрирование по фото)
        list_frame = tk.Frame(self, bg='white')
        list_frame.place(relx=0.5, rely=0.5, anchor='center')
        self.list_canvas = tk.Canvas(list_frame, bg='white', width=600, height=400)
        scrollbar = tk.Scrollbar(list_frame, orient='vertical', command=self.list_canvas.yview)
        self.scrollable_frame = tk.Frame(self.list_canvas, bg='white')
        self.scrollable_frame.bind('<Configure>',
                                   lambda e: self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all")))
        self.list_canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.list_canvas.configure(yscrollcommand=scrollbar.set)
        self.list_canvas.pack(side='left', fill='both')
        scrollbar.pack(side='right', fill='y')

        def _on_mousewheel(event):
            self.list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.list_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.update_checkboxes()

        # Кнопка подтверждения (внизу по фото)
        self.confirm_btn = tk.Button(self, text="Подтвердить отмеченные", bg=self.green, fg='white', font=BODY_FONT,
                                     relief='flat', bd=0, padx=20, pady=10, command=self.confirm_checked)
        self.confirm_btn.pack(side='bottom', pady=20)

        # Добавление (input растянуто, кнопка справа)
        self.add_frame = tk.Frame(self, bg='white')
        self.add_frame.pack(pady=10, fill='x', padx=20)
        tk.Label(self.add_frame, text="Покупка...:", font=BODY_FONT, bg='white').pack(side='left')
        self.shop_entry = tk.Entry(self.add_frame, font=BODY_FONT, relief='flat', bd=1, highlightcolor=self.green)
        self.shop_entry.pack(side='left', fill='x', expand=True, padx=10)  # Растянуто с пробелами
        self.add_btn = tk.Button(self.add_frame, text="Добавить", bg=self.green, fg='white', font=BODY_FONT,
                                 relief='flat', bd=0, width=15,
                                 command=self.add_item)
        self.add_btn.pack(side='right')

    def update_checkboxes(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.shopping_vars = []
        self.check_frames = []

        for idx, item in enumerate(self.items):
            frame = tk.Frame(self.scrollable_frame, bg='white')
            frame.pack(anchor='w', pady=2, fill='x')

            var = tk.BooleanVar(value=item['checked'])
            self.shopping_vars.append(var)
            chk = tk.Checkbutton(frame, text=f"{item['name']}: {item['amount']}", variable=var, bg='white',
                                 font=BODY_FONT, relief='flat')
            chk.pack(side='left', fill='x', expand=True)  # Текст слева с пробелами (expand)

            # Крестик в самом правом краю
            del_btn = tk.Button(frame, text='❌', bg=self.red, fg='white', font=BODY_FONT,
                                relief='flat', bd=0, width=2, command=lambda i=idx: self.delete_item(i))
            del_btn.pack(side='right', padx=0)  # Самый правый край

            self.check_frames.append(frame)

    def confirm_checked(self):
        checked_indices = [i for i, var in enumerate(self.shopping_vars) if var.get()]
        if not checked_indices:
            messagebox.showinfo("OK", "Нет отмеченных товаров!")
            return

        if messagebox.askyesno("Подтвердить", f"Добавить {len(checked_indices)} отмеченных в кладовую?"):
            added = []
            for i in reversed(checked_indices):
                item = self.items[i]
                self.controller.update_pantry_items(
                    self.controller.get_pantry_items() + [{'name': item['name'], 'amount': item['amount']}])
                added.append(item['name'])
                del self.items[i]
                self.shopping_vars.pop(i)

            self.controller.db.save_shopping(self.items)
            self.update_checkboxes()
            messagebox.showinfo("OK", f"Добавлено в кладовую: {', '.join(added)}!")

    def add_item(self):
        new_item = self.shop_entry.get()
        if new_item:
            self.items.append({'name': new_item, 'amount': '', 'checked': False})
            self.controller.db.save_shopping(self.items)
            self.update_checkboxes()
            self.shop_entry.delete(0, tk.END)

    def delete_item(self, idx):
        if messagebox.askyesno("Удалить", f"Удалить {self.items[idx]['name']}?"):
            del self.items[idx]
            self.shopping_vars.pop(idx)
            self.controller.db.save_shopping(self.items)
            self.update_checkboxes()