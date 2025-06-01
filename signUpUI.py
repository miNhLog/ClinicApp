import tkinter as tk
from tkinter import messagebox
from utils import *

USER_FILE = "usersAcc.json"
DOCTOR_FILE = "doctorsAcc.json"

class SignUp:
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.title("Tạo tài khoản mới")
        self.top.geometry("925x500+300+200")
        self.top.configure(bg="#fff")
        self.top.resizable(False, False)

        self.top.transient(master)
        self.top.grab_set() 
        self.top.focus_set()

        self.img = tk.PhotoImage(file='signup.png')
        tk.Label(self.top, image=self.img, bg='white').place(x=50, y=50)

        # Frame cho các thành phần nhập liệu
        self.frame = tk.Frame(self.top, width=350, height=400, bg="white")
        self.frame.place(x=480, y=50)

        # Tiêu đề
        tk.Label(self.frame, text='Tạo tài khoản', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold')).place(x=80, y=5)

        # Hàm xử lý khi focus vào ô nhập liệu
        def on_enter(e):
            if e.widget == self.username_entry:
                if self.username_entry.get() == 'Tên đăng nhập':
                    self.username_entry.delete(0, 'end')
            elif e.widget == self.password_entry:
                if self.password_entry.get() == 'Mật khẩu':
                    self.password_entry.delete(0, 'end')
            elif e.widget == self.confirm_entry:
                if self.confirm_entry.get() == 'Xác nhận mật khẩu':
                    self.confirm_entry.delete(0, 'end')

        # Hàm xử lý khi focus rời khỏi ô nhập liệu
        def on_leave(e):
            if e.widget == self.username_entry:
                if self.username_entry.get() == '':
                    self.username_entry.insert(0, 'Tên đăng nhập')
            elif e.widget == self.password_entry:
                if self.password_entry.get() == '':
                    self.password_entry.insert(0, 'Mật khẩu')
            elif e.widget == self.confirm_entry:
                if self.confirm_entry.get() == '':
                    self.confirm_entry.insert(0, 'Xác nhận mật khẩu')

        # Ô nhập Username
        self.username_entry = tk.Entry(self.frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        self.username_entry.place(x=30, y=80)
        self.username_entry.insert(0, 'Tên đăng nhập')
        self.username_entry.bind('<FocusIn>', on_enter)
        self.username_entry.bind('<FocusOut>', on_leave)
        tk.Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=107)

        # Ô nhập Password
        self.password_entry = tk.Entry(self.frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        self.password_entry.place(x=30, y=150)
        self.password_entry.insert(0, 'Mật khẩu')
        self.password_entry.bind('<FocusIn>', on_enter)
        self.password_entry.bind('<FocusOut>', on_leave)
        tk.Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=177)

        # Ô nhập Confirm Password
        self.confirm_entry = tk.Entry(self.frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        self.confirm_entry.place(x=30, y=220)
        self.confirm_entry.insert(0, 'Xác nhận mật khẩu')
        self.confirm_entry.bind('<FocusIn>', on_enter)
        self.confirm_entry.bind('<FocusOut>', on_leave)
        tk.Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=247)

        # Nút Tạo tài khoản
        tk.Button(self.frame, width=39, pady=7, text='Tạo tài khoản', bg='#57a1f8', fg='white', border=0, command=self.register).place(x=35, y=280)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        # Kiểm tra xem các ô nhập liệu có bị bỏ trống hay không
        if username == 'Tên đăng nhập' or password == 'Mật khẩu' or confirm == 'Xác nhận mật khẩu':
            messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Kiểm tra xem mật khẩu và mật khẩu xác nhận có khớp nhau hay không
        if password != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            return

        # Kiểm tra xem tên người dùng đã tồn tại trong hệ thống hay chưa
        users = load_data(USER_FILE)
        doctors = load_data(DOCTOR_FILE)
        if any(user["username"] == username for user in users) or any(doctor["username"] == username for doctor in doctors):
            messagebox.showerror("Lỗi", "Tên người dùng đã tồn tại!")
            return

        # Lưu tài khoản mới và hoàn tất quá trình đăng ký
        users.append({
            "username": username,
            "password": password,
            "role": "Bệnh nhân"
        })
        save_data(users, USER_FILE)
        messagebox.showinfo("Thành công", "Tạo tài khoản thành công! Bạn có thể đăng nhập.")
        self.top.destroy()
