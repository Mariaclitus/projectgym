import customtkinter as ctk
from tkinter import messagebox
import mysql.connector


# ---------------- DATABASE ----------------

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="gymmanagement"
    )


# ---------------- MARK ATTENDANCE ----------------

def mark_attendance():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        member = member_id.get()
        att_date = date_entry.get()
        att_status = status_box.get()

        if member == "" or att_date == "" or att_status == "":
            messagebox.showwarning("Warning", "Fill all fields!")
            return

        cursor.execute("""
            INSERT INTO attendance
            (member_id, attendance_date, status)
            VALUES (%s,%s,%s)
        """, (member, att_date, att_status))

        conn.commit()

        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Attendance Marked Successfully!")

        member_id.delete(0, "end")
        date_entry.delete(0, "end")
        status_box.set("Present")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- WINDOW ----------------

def open_attendance():
    global member_id, date_entry, status_box

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Attendance Management")
    app.geometry("700x500")

    title = ctk.CTkLabel(
        app,
        text="📅 ATTENDANCE MANAGEMENT",
        font=("Arial", 28, "bold")
    )
    title.pack(pady=20)

    ctk.CTkLabel(
        app,
        text="Member ID"
    ).pack()

    member_id = ctk.CTkEntry(
        app,
        width=300,
        placeholder_text="Enter Member ID"
    )
    member_id.pack(pady=10)

    ctk.CTkLabel(
        app,
        text="Attendance Date (YYYY-MM-DD)"
    ).pack()

    date_entry = ctk.CTkEntry(
        app,
        width=300,
        placeholder_text="2026-07-13"
    )
    date_entry.pack(pady=10)

    ctk.CTkLabel(
        app,
        text="Status"
    ).pack()

    status_box = ctk.CTkComboBox(
        app,
        values=["Present", "Absent"],
        width=300
    )
    status_box.set("Present")
    status_box.pack(pady=10)

    ctk.CTkButton(
        app,
        text="Mark Attendance",
        command=mark_attendance,
        width=200
    ).pack(pady=20)

    app.mainloop()


# ---------------- MAIN ----------------

if __name__ == "__main__":
    open_attendance()