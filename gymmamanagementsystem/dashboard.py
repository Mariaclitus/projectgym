import customtkinter as ctk

from members import open_members
from trainers import open_trainers
from payments import open_payments
from attendance import open_attendance
from reports import open_reports


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


def open_dashboard():

    dashboard = ctk.CTk()
    dashboard.title("Gym Management Dashboard")
    dashboard.geometry("1000x650")

    title = ctk.CTkLabel(
        dashboard,
        text="🏋️ Gym Management Dashboard",
        font=("Arial", 30, "bold")
    )
    title.pack(pady=30)

    members_btn = ctk.CTkButton(
        dashboard,
        text="👥 Members",
        width=250,
        height=50,
        command=open_members
    )
    members_btn.pack(pady=10)

    trainers_btn = ctk.CTkButton(
        dashboard,
        text="🏋️ Trainers",
        width=250,
        height=50,
        command=open_trainers
    )
    trainers_btn.pack(pady=10)

    payments_btn = ctk.CTkButton(
        dashboard,
        text="💳 Payments",
        width=250,
        height=50,
        command=open_payments
    )
    payments_btn.pack(pady=10)

    attendance_btn = ctk.CTkButton(
        dashboard,
        text="📅 Attendance",
        width=250,
        height=50,
        command=open_attendance
    )
    attendance_btn.pack(pady=10)

    reports_btn = ctk.CTkButton(
        dashboard,
        text="📊 Reports",
        width=250,
        height=50,
        command=open_reports
    )
    reports_btn.pack(pady=10)

    dashboard.mainloop()


if __name__ == "__main__":
    open_dashboard()