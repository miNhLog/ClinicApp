import tkinter as tk
from tkinter import ttk
from utils import load_data

DOCTOR_FILE = "doctorsAcc.json"

class DoctorUI:
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.configure(bg="#ffe4e1")  # Màu nền hồng nhạt
        self.top.title("Tìm bác sĩ")
        self.top.geometry("800x500")

        self.doctors = load_data(DOCTOR_FILE)
        self.specialties = sorted(list(set(doctor["specialty"] for doctor in self.doctors)))
        self.specialties.insert(0, "Chọn")

        self.top.transient(master)
        self.top.grab_set()
        self.top.focus_set()

        self.create_doctor_view()

    def create_doctor_view(self):
        search_frame = tk.Frame(self.top, bg="#ffe4e1")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Tìm theo họ tên:", bg="#ffe4e1", font=("Helvetica", 10)).pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(search_frame)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(search_frame, text="Chọn chuyên khoa:", bg="#ffe4e1", font=("Helvetica", 10)).pack(side=tk.LEFT, padx=5)
        self.specialty_combobox = ttk.Combobox(search_frame, values=self.specialties, state="readonly")
        self.specialty_combobox.set("Chọn")
        self.specialty_combobox.pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Tìm bác sĩ", command=self.search_doctors, bg="#FF9999").pack(side=tk.LEFT, padx=5)

        tk.Label(self.top, text="Danh sách bác sĩ", font=("Helvetica", 14, "bold"), bg="#ffe4e1").pack(pady=10)

        columns = ("Tên", "Chuyên khoa", "Email", "Số điện thoại")
        self.tree = ttk.Treeview(self.top, columns=columns, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Chuyên khoa", text="Chuyên khoa")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Số điện thoại", text="Số điện thoại")

        self.tree.column("Tên", width=200)
        self.tree.column("Chuyên khoa", width=150)
        self.tree.column("Email", width=200)
        self.tree.column("Số điện thoại", width=150)

        scrollbar = ttk.Scrollbar(self.top, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.display_doctors()

        tk.Button(self.top, text="Đóng", command=self.top.destroy, bg="#FF9999").pack(pady=10)

    def display_doctors(self, name_filter=None, specialty_filter=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for doctor in self.doctors:
            name = doctor["name"]
            specialty = doctor["specialty"]
            
            name_match = name_filter is None or name_filter.lower() in name.lower()
            specialty_match = specialty_filter is None or specialty_filter == "Chọn" or specialty == specialty_filter
            
            if name_match and specialty_match:
                self.tree.insert("", tk.END, values=(
                    name,
                    specialty,
                    doctor["email"],
                    doctor["phone"]
                ))

    def search_doctors(self):
        name_filter = self.name_entry.get().strip()
        specialty_filter = self.specialty_combobox.get()
        
        if not name_filter and specialty_filter == "Chọn":
            self.display_doctors()
            return
            
        if not name_filter:
            name_filter = None
            
        self.display_doctors(name_filter, specialty_filter)