"""Общие элементы UI: кастомное подтверждение деструктивных действий (без блокировки стиля приложения)."""

import tkinter as tk
from tkinter import ttk

from config import BODY_FONT, HEADER_FONT, RED


def confirm_destructive(
    parent,
    title: str,
    message: str,
    detail: str | None = None,
    *,
    confirm_text: str = "Удалить",
    cancel_text: str = "Отмена",
    danger_color: str = RED,
):
    """
    Модальное окно подтверждения с явным разделением безопасной и опасной кнопки.
    Возвращает True, если пользователь подтвердил деструктивное действие.
    """
    root = parent.winfo_toplevel()
    dlg = tk.Toplevel(root)
    dlg.title(title)
    dlg.transient(root)
    dlg.grab_set()
    dlg.configure(bg="white")
    dlg.resizable(False, False)

    result = {"ok": False}

    def on_cancel():
        result["ok"] = False
        dlg.destroy()

    def on_confirm():
        result["ok"] = True
        dlg.destroy()

    frm = tk.Frame(dlg, bg="white", padx=24, pady=20)
    frm.pack(fill="both", expand=True)

    tk.Label(frm, text=message, font=HEADER_FONT, bg="white", wraplength=420, justify="left").pack(anchor="w")
    if detail:
        tk.Label(
            frm,
            text=detail,
            font=BODY_FONT,
            fg="#616161",
            bg="white",
            wraplength=420,
            justify="left",
        ).pack(anchor="w", pady=(8, 16))
    else:
        tk.Frame(frm, height=8, bg="white").pack()

    btn_row = tk.Frame(frm, bg="white")
    btn_row.pack(fill="x", pady=(12, 0))

    ttk.Button(btn_row, text=cancel_text, width=14, command=on_cancel).pack(side="right", padx=(8, 0))
    tk.Button(
        btn_row,
        text=confirm_text,
        bg=danger_color,
        fg="white",
        font=BODY_FONT,
        relief="flat",
        padx=16,
        pady=8,
        cursor="hand2",
        command=on_confirm,
    ).pack(side="right")

    dlg.protocol("WM_DELETE_WINDOW", on_cancel)
    dlg.update_idletasks()
    x = root.winfo_rootx() + (root.winfo_width() - dlg.winfo_reqwidth()) // 2
    y = root.winfo_rooty() + (root.winfo_height() - dlg.winfo_reqheight()) // 2
    dlg.geometry(f"+{max(0, x)}+{max(0, y)}")

    dlg.wait_window()
    return result["ok"]
