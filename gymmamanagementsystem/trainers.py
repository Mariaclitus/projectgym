import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector

# ---------------- DATABASE ----------------

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="gymmanagement"
    )

# ---------------- LOAD ----------------

def load_trainers():

    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT trainer_id,
               trainer_name,
               specialization,
               phone,
               salary
        FROM trainers
        ORDER BY trainer_id DESC
    """)

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)

    conn.close()

# ---------------- CLEAR ----------------

def clear_fields():
    name_entry.delete(0, "end")
    specialization_entry.delete(0, "end")
    phone_entry.delete(0, "end")
    salary_entry.delete(0, "end")

# ---------------- ADD ----------------

def add_trainer():

    if name_entry.get() == "":
        messagebox.showwarning("Warning", "Enter Trainer Name")
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trainers
        (trainer_name,specialization,phone,salary)
        VALUES(%s,%s,%s,%s)
    """,(
        name_entry.get(),
        specialization_entry.get(),
        phone_entry.get(),
        salary_entry.get()
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success","Trainer Added")

    clear_fields()
    load_trainers()

# ---------------- DELETE ----------------

def delete_trainer():

    selected = tree.focus()

    if selected == "":
        messagebox.showwarning("Warning","Select Trainer")
        return

    values = tree.item(selected,"values")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM trainers WHERE trainer_id=%s",
        (values[0],)
    )

    conn.commit()
    conn.close()

    load_trainers()
    clear_fields()

# ---------------- UPDATE ----------------

def update_trainer():

    selected = tree.focus()

    if selected == "":
        messagebox.showwarning("Warning","Select Trainer")
        return

    trainer_id = tree.item(selected)["values"][0]

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE trainers
        SET trainer_name=%s,
            specialization=%s,
            phone=%s,
            salary=%s
        WHERE trainer_id=%s
    """,(
        name_entry.get(),
        specialization_entry.get(),
        phone_entry.get(),
        salary_entry.get(),
        trainer_id
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo("Success","Updated Successfully")

    load_trainers()

# ---------------- SEARCH ----------------

def search_trainer():

    keyword = search_entry.get()

    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM trainers
        WHERE trainer_name LIKE %s
    """,('%'+keyword+'%',))

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", "end", values=row)

    conn.close()

# ---------------- SELECT ----------------

def select_record(event):

    selected = tree.focus()

    if selected == "":
        return

    values = tree.item(selected)["values"]

    clear_fields()

    name_entry.insert(0, values[1])
    specialization_entry.insert(0, values[2])
    phone_entry.insert(0, values[3])
    salary_entry.insert(0, values[4])

# ---------------- WINDOW ----------------

def open_trainers():

    global tree
    global name_entry
    global specialization_entry
    global phone_entry
    global salary_entry
    global search_entry

    trainers = ctk.CTkToplevel()
    trainers.title("Trainer Management")
    trainers.geometry("1000x650")

    title = ctk.CTkLabel(
        trainers,
        text="🏋 TRAINER MANAGEMENT",
        font=("Arial",28,"bold")
    )
    title.pack(pady=15)

    frame = ctk.CTkFrame(trainers)
    frame.pack(pady=10)

    ctk.CTkLabel(frame,text="Trainer Name").grid(row=0,column=0,padx=10,pady=5)

    name_entry = ctk.CTkEntry(frame,width=220)
    name_entry.grid(row=0,column=1)

    ctk.CTkLabel(frame,text="Specialization").grid(row=1,column=0,padx=10,pady=5)

    specialization_entry = ctk.CTkEntry(frame,width=220)
    specialization_entry.grid(row=1,column=1)

    ctk.CTkLabel(frame,text="Phone").grid(row=2,column=0,padx=10,pady=5)

    phone_entry = ctk.CTkEntry(frame,width=220)
    phone_entry.grid(row=2,column=1)

    ctk.CTkLabel(frame,text="Salary").grid(row=3,column=0,padx=10,pady=5)

    salary_entry = ctk.CTkEntry(frame,width=220)
    salary_entry.grid(row=3,column=1)

    ctk.CTkButton(frame,text="Add",command=add_trainer,width=120).grid(row=4,column=0,pady=15)

    ctk.CTkButton(frame,text="Update",command=update_trainer,width=120).grid(row=4,column=1)

    ctk.CTkButton(frame,text="Delete",command=delete_trainer,width=120).grid(row=5,column=0,pady=10)

    ctk.CTkButton(frame,text="Clear",command=clear_fields,width=120).grid(row=5,column=1)

    search_frame = ctk.CTkFrame(trainers)
    search_frame.pack(pady=10)

    search_entry = ctk.CTkEntry(search_frame,width=250,placeholder_text="Search Trainer")
    search_entry.pack(side="left",padx=10)

    ctk.CTkButton(search_frame,text="Search",command=search_trainer).pack(side="left")

    tree = ttk.Treeview(
        trainers,
        columns=("ID","Name","Specialization","Phone","Salary"),
        show="headings",
        height=12
    )

    for col in ("ID","Name","Specialization","Phone","Salary"):
        tree.heading(col,text=col)

    tree.column("ID",width=60)
    tree.column("Name",width=200)
    tree.column("Specialization",width=180)
    tree.column("Phone",width=150)
    tree.column("Salary",width=120)

    tree.pack(fill="both",expand=True,padx=20,pady=20)

    tree.bind("<ButtonRelease-1>", select_record)

    load_trainers()

# ---------------- MAIN ----------------

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.withdraw()

    open_trainers()

    root.mainloop()