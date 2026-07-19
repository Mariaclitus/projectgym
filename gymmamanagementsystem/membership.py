import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, timedelta

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ---------------- DATABASE ---------------- #

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="gymmanagement"
    )


# ---------------- LOAD MEMBERS ---------------- #

def load_members():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT member_id, name FROM members")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# ---------------- LOAD PLANS ---------------- #

def load_plans():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT plan_id, plan_name
        FROM membershipplans
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# ---------------- LOAD MEMBERSHIPS ---------------- #

def load_memberships():

    global tree

    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            membership_id,
            member_id,
            plan_id,
            start_date,
            end_date
        FROM memberships
        ORDER BY membership_id DESC
    """)

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)

    cursor.close()
    conn.close()
    # ---------------- ADD MEMBERSHIP ---------------- #

def add_membership():

    try:

        member_id = int(member_box.get().split(" - ")[0])
        plan_id = int(plan_box.get().split(" - ")[0])

        start_date = start_entry.get()
        end_date = end_entry.get()

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO memberships
            (member_id, plan_id, start_date, end_date)
            VALUES (%s, %s, %s, %s)
        """, (member_id, plan_id, start_date, end_date))

        conn.commit()

        cursor.close()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Membership Added Successfully!"
        )

        load_memberships()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- MEMBERSHIP WINDOW ---------------- #

def open_membership():

    global member_box
    global plan_box
    global start_entry
    global end_entry
    global tree

    app = ctk.CTk()

    app.title("Membership Management")
    app.geometry("1000x700")

    title = ctk.CTkLabel(
        app,
        text="💳 MEMBERSHIP MANAGEMENT",
        font=("Arial", 28, "bold")
    )
    title.pack(pady=20)

    ctk.CTkLabel(
        app,
        text="Member"
    ).pack()

    member_values = [
        f"{m[0]} - {m[1]}"
        for m in load_members()
    ]

    member_box = ctk.CTkComboBox(
        app,
        values=member_values,
        width=300
    )
    member_box.pack(pady=5)

    ctk.CTkLabel(
        app,
        text="Membership Plan"
    ).pack()

    plan_values = [
        f"{p[0]} - {p[1]}"
        for p in load_plans()
    ]

    plan_box = ctk.CTkComboBox(
        app,
        values=plan_values,
        width=300
    )
    plan_box.pack(pady=5)

    ctk.CTkLabel(
        app,
        text="Start Date (YYYY-MM-DD)"
    ).pack()

    start_entry = ctk.CTkEntry(
        app,
        width=300
    )
    start_entry.pack(pady=5)

    ctk.CTkLabel(
        app,
        text="End Date (YYYY-MM-DD)"
    ).pack()

    end_entry = ctk.CTkEntry(
        app,
        width=300
    )
    end_entry.pack(pady=5)
    add_btn = ctk.CTkButton(
        app,
        text="Add Membership",
        width=200,
        command=add_membership
    )
    add_btn.pack(pady=20)

    # ---------------- TABLE ---------------- #

    tree = ttk.Treeview(
        app,
        columns=(
    "Membership ID",
    "Member Name",
    "Plan Name",
    "Start Date",
    "End Date"
)
        ),
        show="headings",
        height=12
)

    tree.heading("Membership ID", text="Membership ID")
    tree.heading("Member Name", text="Member Name")
    tree.heading("Plan Name", text="Plan Name")
    tree.heading("Start Date", text="Start Date")
    tree.heading("End Date", text="End Date")

    tree.column("Membership ID", width=120)
    tree.column("Member Name", width=180)
    tree.column("Plan Name", width=180)
    tree.column("Start Date", width=150)
    tree.column("End Date", width=150)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    load_memberships()
    def load_memberships():

    global tree

    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ms.membership_id,
            m.name,
            mp.plan_name,
            ms.start_date,
            ms.end_date
        FROM memberships ms
        JOIN members m
            ON ms.member_id = m.member_id
        JOIN membershipplans mp
            ON ms.plan_id = mp.plan_id
        ORDER BY ms.membership_id DESC
    """)

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)

    cursor.close()
    conn.close()


    app.mainloop()


if __name__ == "__main__":
    open_membership()