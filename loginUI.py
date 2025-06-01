import tkinter as tk
from tkinter import messagebox
from utils import *
from main import ClinicApp
from signUpUI import SignUp

USER_FILE = "usersAcc.json"
DOCTOR_FILE = "doctorsAcc.json"


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập hệ thống")
        self.root.geometry("925x500")
        self.root.configure(bg="#fff")
        self.root.resizable(False, False)

        # Tải hình ảnh
        self.img = tk.PhotoImage(file='login.png')
        tk.Label(root, image=self.img, bg='white').place(x=50, y=50)

        # Frame cho các thành phần nhập liệu
        self.frame = tk.Frame(root, width=350, height=350, bg="white")
        self.frame.place(x=480, y=70)

        # Tiêu đề
        tk.Label(self.frame, text='Đăng nhập', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold')).place(x=100, y=5)

        # Hàm xử lý khi focus vào ô nhập liệu
        def on_enter(e):
            if e.widget == self.username_entry:
                self.username_entry.delete(0, 'end')
            elif e.widget == self.password_entry:
                self.password_entry.delete(0, 'end')

        # Hàm xử lý khi focus rời khỏi ô nhập liệu
        def on_leave(e):
            if e.widget == self.username_entry:
                name = self.username_entry.get()
                if name == '':
                    self.username_entry.insert(0, 'Tên đăng nhập')
            elif e.widget == self.password_entry:
                name = self.password_entry.get()
                if name == '':
                    self.password_entry.insert(0, 'Mật khẩu')

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

        # Nút Đăng nhập
        tk.Button(self.frame, width=39, pady=7, text='Đăng nhập', bg='#57a1f8', fg='white', border=0, command=self.login).place(x=35, y=204)

        # Nhãn "Tạo tài khoản mới"
        tk.Label(self.frame, text="Bạn chưa có tài khoản?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9)).place(x=75, y=270)
        sign_up = tk.Button(self.frame, width=6, text='Đăng ký', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=self.open_register)
        sign_up.place(x=215, y=270)

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        users = load_data(USER_FILE)
        doctors = load_data(DOCTOR_FILE)
        for user in users:
            if user["username"] == username and user["password"] == password:
                messagebox.showinfo("Thành công", f"Đăng nhập với vai trò {user['role']}")
                # Xóa nội dung cửa sổ đăng nhập
                for widget in self.root.winfo_children():
                    widget.destroy()
                # Khởi tạo giao diện chính trong cùng cửa sổ root
                app = ClinicApp(self.root, username, user['role'])
                return

        for doctor in doctors:
            if doctor["username"] == username and doctor["password"] == password:
                messagebox.showinfo("Thành công", f"Đăng nhập với vai trò Bác sĩ")
                # Xóa nội dung cửa sổ đăng nhập
                for widget in self.root.winfo_children():
                    widget.destroy()
                # Khởi tạo giao diện chính trong cùng cửa sổ root
                app = ClinicApp(self.root, username, "Bác sĩ")
                return

        messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

    def open_register(self):
        SignUp(self.root)
