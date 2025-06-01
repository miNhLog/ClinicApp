import tkinter as tk
from tkinter import ttk, messagebox
from utils import load_data

USER_FILE = "usersAcc.json"
DOCTOR_FILE = "doctorsAcc.json"

class AccountUI:
    def __init__(self, master):

        self.top = tk.Toplevel(master)
        self.top.configure(bg="#ffe4e1")
        self.top.title("Quản lý tài khoản")
        self.top.geometry("600x500")

        # Tải dữ liệu tài khoản
        self.users = load_data(USER_FILE)
        self.doctors = load_data(DOCTOR_FILE)

        self.create_account_view()

    def create_account_view(self):
        tk.Label(self.top, text="Danh sách tài khoản",bg="#ffe4e1", font=("Helvetica", 14, "bold")).pack(pady=10)

        tk.Label(self.top, text="Tìm kiếm theo tên đăng nhập:",bg="#ffe4e1").pack()
        self.search_entry = tk.Entry(self.top)
        self.search_entry.pack(pady=5)
        
        # Frame cho các nút tìm kiếm
        search_button_frame = tk.Frame(self.top)
        search_button_frame.pack(pady=5)
        tk.Button(search_button_frame, text="Tìm kiếm",bg="#FF9999", command=self.search_accounts).pack()

        # Tạo Treeview để hiển thị tài khoản
        columns = ("Tên đăng nhập", "Mật khẩu", "Vai trò")
        self.tree = ttk.Treeview(self.top, columns=columns, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Đặt tiêu đề cột
        self.tree.heading("Tên đăng nhập", text="Tên đăng nhập")
        self.tree.heading("Mật khẩu", text="Mật khẩu")
        self.tree.heading("Vai trò", text="Vai trò")

        # Đặt độ rộng cột
        self.tree.column("Tên đăng nhập", width=200)
        self.tree.column("Mật khẩu", width=200)
        self.tree.column("Vai trò", width=150)

        # Thêm thanh cuộn
        scrollbar = ttk.Scrollbar(self.top, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Hiển thị tất cả tài khoản
        self.display_accounts()

        # Nút đóng
        tk.Button(self.top, text="Đóng",bg="#FF9999", command=self.top.destroy).pack(pady=10)

    def display_accounts(self, search_term=None):
        # Xóa dữ liệu cũ trong Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Hiển thị tài khoản bệnh nhân
        for user in self.users:
            if user["role"] != "Admin": 
                if search_term is None or search_term.lower() in user["username"].lower():
                    self.tree.insert("", tk.END, values=(
                        user["username"],
                        user["password"],
                        user["role"]
                    ))

        # Hiển thị tài khoản bác sĩ
        for doctor in self.doctors:
            if search_term is None or search_term.lower() in doctor["username"].lower():
                self.tree.insert("", tk.END, values=(
                    doctor["username"],
                    doctor["password"],
                    "Bác sĩ"
                ))

    def search_accounts(self):
        search_term = self.search_entry.get().strip()
        self.display_accounts(search_term)
