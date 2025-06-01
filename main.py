import tkinter as tk
from tkinter import messagebox
from loginUI import *
from appointmentUI import AppointmentUI
from viewScheduleUI import ViewScheduleUI
from accountUI import AccountUI
from doctorUI import DoctorUI

class ClinicApp:
    def __init__(self, root, username, role):
        self.root = root
        self.username = username
        self.role = role
        self.root.title("Hệ thống Quản lý Phòng khám")
        self.root.geometry("925x500")

        self.bg_image = tk.PhotoImage(file="background.png")
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0)

        self.frame = tk.Frame(self.root, width=400, height=500, bg="#ffe4e1")
        self.frame.place(x=525, y=0)

        self.create_main_menu()

    def manage_account(self):
        AccountUI(self.root)

    def find_doctor(self):
        DoctorUI(self.root)

    def view_schedule(self):
        ViewScheduleUI(self.root, self.username, self.role)

    def make_appointment(self):
        AppointmentUI(self.root, self.username)

    def exit_button(self):
        tk.Button(self.frame, text="Thoát", width=39, pady=7, bg="#8b0000", fg='white',
                  border=0, command=self.root.destroy).place(relx=0.5, y=340, anchor="center")

    def create_main_menu(self):
        btn_bg = "#c94c4c" 
        btn_fg = "white"

        title = tk.Label(self.frame, text=f"Hello {self.username}", 
                 fg="#c94c4c", bg='#ffe4e1', 
                 font=('Segoe UI', 20, 'bold'))
        title.place(relx=0.5, y=50, anchor="center")

        if self.role == "Admin":
            tk.Button(self.frame, text="Quản lý lịch hẹn", width=39, pady=7, bg=btn_bg, fg=btn_fg,
                      border=0, command=self.view_schedule).place(relx= 0.5, y=100, anchor="center")
            tk.Button(self.frame, text="Quản lý tài khoản", width=39, pady=7, bg=btn_bg, fg=btn_fg,
                      border=0, command=self.manage_account).place(relx= 0.5, y=160, anchor="center")
            tk.Button(self.frame, text="Tìm bác sĩ", width=39, pady=7, bg=btn_bg, fg=btn_fg,
                      border=0, command=self.find_doctor).place(relx= 0.5, y=220, anchor="center")
            self.exit_button()

        elif self.role == "Bác sĩ":
            tk.Button(self.frame, text="Xem lịch hẹn", width=39, pady=7, bg=btn_bg, fg=btn_fg,
                      border=0, command=self.view_schedule).place(relx=0.5, y=100, anchor="center")
            self.exit_button()

        elif self.role == "Bệnh nhân":
            tk.Button(self.frame, text="Tìm bác sĩ", width=39, pady=7, bg=btn_bg, fg=btn_fg,
                      border=0, command=self.find_doctor).place(relx= 0.5, y=100, anchor="center")
            tk.Button(self.frame, text="Đặt lịch khám", width=39, pady=7, bg=btn_bg, fg=btn_fg,
                      border=0, command=self.make_appointment).place(relx= 0.5, y=160, anchor="center")
            tk.Button(self.frame, text="Xem lịch hẹn", width=39, pady=7, bg=btn_bg, fg=btn_fg,
                      border=0, command=self.view_schedule).place(relx= 0.5, y=220, anchor="center")
            self.exit_button()

if __name__ == "__main__":
    root = tk.Tk()
    Login(root)
    root.mainloop()
