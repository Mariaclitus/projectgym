import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ---------------- DATABASE CONNECTION ----------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",   # <-- Change this
        database="gymmanagement"
    )


# ---------------- LOGIN FUNCTION ----------------
def login(): 

    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please enter Username and Password")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM login WHERE username=%s AND password=%s",
            (username, password)
        )

        row = cursor.fetchone()

        if row:

            messagebox.showinfo("Success", "Login Successful")

            root.destroy()

            from dashboard import open_dashboard
            open_dashboard()

        else:
            messagebox.showerror("Error", "Invalid Username or Password")

        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))


# ---------------- WINDOW ----------------
root = ctk.CTk()

root.title("Gym Management Login")
root.geometry("500x450")
root.resizable(False, False)

title = ctk.CTkLabel(
    root,
    text="GYM MANAGEMENT SYSTEM",
    font=("Arial", 26, "bold")
)
title.pack(pady=30)

username_entry = ctk.CTkEntry(
    root,
    width=300,
    height=40,
    placeholder_text="Username"
)
username_entry.pack(pady=15)

password_entry = ctk.CTkEntry(
    root,
    width=300,
    height=40,
    placeholder_text="Password",
    show="*"
)
password_entry.pack(pady=15)

login_btn = ctk.CTkButton(
    root,
    text="LOGIN",
    width=200,
    height=40,
    command=login
)
login_btn.pack(pady=30)

root.mainloop()