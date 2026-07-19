from tkinter import ttk, messagebox
import customtkinter as ctk
import mysql.connector

tree = None


def add_member(name, age, gender, phone, join_date):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="gymmanagement"
        )

        cursor = conn.cursor()

        query = """
        INSERT INTO members(name, age, gender, phone, join_date)
        VALUES(%s,%s,%s,%s,%s)
        """

        cursor.execute(query, (name, age, gender, phone, join_date))
        conn.commit()

        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Member Added Successfully!")

        load_members()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def load_members():
    global tree

    for row in tree.get_children():
        tree.delete(row)

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="gymmanagement"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT member_id,name,age,gender,phone,join_date
    FROM members
    """)

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)

    cursor.close()
    conn.close()


def open_members():
    global tree

    members = ctk.CTk()
    members.title("Members Management")
    members.geometry("1000x700")

    title = ctk.CTkLabel(
        members,
        text="👥 MEMBERS MANAGEMENT",
        font=("Arial", 28, "bold")
    )
    title.pack(pady=20)

    ctk.CTkLabel(members, text="Name").pack()
    name_entry = ctk.CTkEntry(members, width=300)
    name_entry.pack(pady=5)

    ctk.CTkLabel(members, text="Age").pack()
    age_entry = ctk.CTkEntry(members, width=300)
    age_entry.pack(pady=5)

    ctk.CTkLabel(members, text="Gender").pack()
    gender_entry = ctk.CTkEntry(members, width=300)
    gender_entry.pack(pady=5)

    ctk.CTkLabel(members, text="Phone").pack()
    phone_entry = ctk.CTkEntry(members, width=300)
    phone_entry.pack(pady=5)

    ctk.CTkLabel(members, text="Join Date (YYYY-MM-DD)").pack()
    join_entry = ctk.CTkEntry(members, width=300)
    join_entry.pack(pady=5)

    ctk.CTkButton(
        members,
        text="Add Member",
        command=lambda: add_member(
            name_entry.get(),
            age_entry.get(),
            gender_entry.get(),
            phone_entry.get(),
            join_entry.get()
        )
    ).pack(pady=20)

    tree = ttk.Treeview(
        members,
        columns=("ID", "Name", "Age", "Gender", "Phone", "Join Date"),
        show="headings"
    )

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Gender", text="Gender")
    tree.heading("Phone", text="Phone")
    tree.heading("Join Date", text="Join Date")

    tree.column("ID", width=60)
    tree.column("Name", width=150)
    tree.column("Age", width=60)
    tree.column("Gender", width=100)
    tree.column("Phone", width=150)
    tree.column("Join Date", width=150)

    tree.pack(fill="both", expand=True, pady=20)

    load_members()

    members.mainloop()


if __name__ == "__main__":
    open_members()