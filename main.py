import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2

DB = {"host":"localhost", "database":"postgres", "user":"postgres", "password":"postgres", "port":"5432"}
user_data = {}
root = tk.Tk()
root.geometry("1000x700")
root.configure(bg="white")

def show_login():
    for w in root.winfo_children(): w.destroy()
    root.title("Авторизация - Чудо Обувь")
    tk.Label(root, text="Вход в систему", font=("Arial", 20), bg="white").pack(pady=50)
    e_log = tk.Entry(root, font=("Arial", 14))
    e_log.pack(pady=10)

    def login():
        conn = psycopg2.connect(**DB)
        cur = conn.cursor()
        cur.execute("SELECT user_id, last_name, first_name, role_id FROM users WHERE login=%s", (e_log.get(),))
        res = cur.fetchone()
        conn.close()
        if res:
            user_data.update({'id': res[0], 'fio': f"{res[1]} {res[2]}", 'role': res[3]})
            show_catalog()
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")

    tk.Button(root, text="Войти", command=login, font=("Arial", 14), bg="#70B2AF", fg="white").pack(pady=20)

def show_catalog():
    for w in root.winfo_children(): w.destroy()
    root.title("Каталог - Чудо Обувь")

    header = tk.Frame(root, bg="#D2F6E7", height=50)
    header.pack(fill="x")
    tk.Label(header, text=f"Пользователь: {user_data['fio']}", font=("Arial", 12), bg="#D2F6E7").pack(side="right", padx=10)

    canvas = tk.Canvas(root, bg="white")
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    conn = psycopg2.connect(**DB)
    cur = conn.cursor()
    cur.execute("SELECT product_id, product_name, price, category FROM products")
    for row in cur.fetchall():
        card = tk.Frame(scroll_frame, bg="white", relief="solid", bd=1)
        card.pack(fill="x", padx=10, pady=5)
        tk.Label(card, text=f"{row[1]} | {row[3]}", font=("Arial", 12), bg="white").pack(anchor="w", padx=10, pady=5)
        tk.Label(card, text=f"Цена: {row[2]} руб.", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=10)
    conn.close()

show_login()
root.mainloop()
