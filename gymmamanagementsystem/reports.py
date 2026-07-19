
# reports.py
# Starter professional reports dashboard for Gym Management System.
# Replace/extend chart queries as needed.

import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="gymmanagement"
    )


class ReportsDashboard:

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Gym Analytics Dashboard")
        self.root.geometry("1400x850")

        title = ctk.CTkLabel(
            self.root,
            text="📊 GYM ANALYTICS DASHBOARD",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=15)

        cards = ctk.CTkFrame(self.root)
        cards.pack(fill="x", padx=15)

        self.member_lbl = self.make_card(cards, "Members", 0)
        self.trainer_lbl = self.make_card(cards, "Trainers", 1)
        self.revenue_lbl = self.make_card(cards, "Revenue", 2)
        self.att_lbl = self.make_card(cards, "Attendance", 3)

        charts = ctk.CTkFrame(self.root)
        charts.pack(fill="both", expand=True, padx=15, pady=15)

        self.pie = ctk.CTkFrame(charts)
        self.bar = ctk.CTkFrame(charts)
        self.line = ctk.CTkFrame(charts)
        self.column = ctk.CTkFrame(charts)

        self.pie.grid(row=0,column=0,padx=10,pady=10)
        self.bar.grid(row=0,column=1,padx=10,pady=10)
        self.line.grid(row=1,column=0,padx=10,pady=10)
        self.column.grid(row=1,column=1,padx=10,pady=10)

        ctk.CTkButton(
            self.root,
            text="Refresh",
            command=self.load_dashboard
        ).pack(pady=10)

        self.load_dashboard()
        self.root.mainloop()

    def make_card(self,parent,title,col):
        f=ctk.CTkFrame(parent,width=250,height=100)
        f.grid(row=0,column=col,padx=10,pady=10)
        ctk.CTkLabel(f,text=title,font=("Arial",18,"bold")).pack(pady=5)
        v=ctk.CTkLabel(f,text="0",font=("Arial",26,"bold"))
        v.pack()
        return v

    def load_dashboard(self):
        try:
            conn=connect_db()
            cur=conn.cursor()

            cur.execute("SELECT COUNT(*) FROM members")
            m=cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM trainers")
            t=cur.fetchone()[0]
            cur.execute("SELECT IFNULL(SUM(amount),0) FROM payments")
            r=cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM attendance")
            a=cur.fetchone()[0]

            self.member_lbl.configure(text=str(m))
            self.trainer_lbl.configure(text=str(t))
            self.revenue_lbl.configure(text=f"₹{r}")
            self.att_lbl.configure(text=str(a))

            conn.close()

            self.gender_chart()
            self.salary_chart()

        except Exception as e:
            messagebox.showerror("Database Error",str(e))

    def clear(self,frame):
        for w in frame.winfo_children():
            w.destroy()

    def gender_chart(self):
        self.clear(self.pie)
        conn=connect_db()
        cur=conn.cursor()
        cur.execute("SELECT gender,COUNT(*) FROM members GROUP BY gender")
        data=cur.fetchall()
        conn.close()
        if not data:
            return
        labels=[x[0] for x in data]
        values=[x[1] for x in data]
        fig=Figure(figsize=(5,4),dpi=100)
        ax=fig.add_subplot(111)
        ax.pie(values,labels=labels,autopct="%1.1f%%")
        ax.set_title("Gender Distribution")
        canvas=FigureCanvasTkAgg(fig,self.pie)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both",expand=True)

    def salary_chart(self):
        self.clear(self.bar)
        conn=connect_db()
        cur=conn.cursor()
        cur.execute("SELECT trainer_name,salary FROM trainers")
        data=cur.fetchall()
        conn.close()
        if not data:
            return
        names=[x[0] for x in data]
        vals=[float(x[1] or 0) for x in data]
        fig=Figure(figsize=(5,4),dpi=100)
        ax=fig.add_subplot(111)
        ax.bar(names,vals)
        ax.tick_params(axis="x",rotation=45)
        ax.set_title("Trainer Salary")
        canvas=FigureCanvasTkAgg(fig,self.bar)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both",expand=True)
def open_reports():
    ReportsDashboard()


if __name__ == "__main__":
    ReportsDashboard()

