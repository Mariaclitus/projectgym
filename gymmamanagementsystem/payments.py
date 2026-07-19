import customtkinter as ctk
import mysql.connector
from tkinter import messagebox


def add_payment():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="gymmanagement"
        )

        cursor = conn.cursor()

        sql = """
        INSERT INTO payments (member_id, amount, payment_date)
        VALUES (%s, %s, %s)
        """

        values = (
            int(member_id.get()),
            float(amount.get()),
            payment_date.get()
        )

        cursor.execute(sql, values)
        conn.commit()

        messagebox.showinfo("Success", "Payment Added Successfully!")

        member_id.delete(0, "end")
        amount.delete(0, "end")
        payment_date.delete(0, "end")

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))


def open_payments():
    global member_id, amount, payment_date

    payments = ctk.CTk()
    payments.title("Payments Management")
    payments.geometry("1000x600")

    title = ctk.CTkLabel(
        payments,
        text="💳 PAYMENTS MANAGEMENT",
        font=("Arial", 28, "bold")
    )
    title.pack(pady=20)

    member_id = ctk.CTkEntry(
        payments,
        width=300,
        placeholder_text="Member ID"
    )
    member_id.pack(pady=10)

    amount = ctk.CTkEntry(
        payments,
        width=300,
        placeholder_text="Amount"
    )
    amount.pack(pady=10)

    payment_date = ctk.CTkEntry(
        payments,
        width=300,
        placeholder_text="Payment Date (YYYY-MM-DD)"
    )
    payment_date.pack(pady=10)

    add_btn = ctk.CTkButton(
        payments,
        text="Add Payment",
        command=add_payment
    )
    add_btn.pack(pady=20)

    payments.mainloop()


if __name__ == "__main__":
    open_payments()