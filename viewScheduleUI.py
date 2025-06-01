import tkinter as tk
from tkinter import ttk, messagebox
from utils import load_data, save_data

APPOINTMENT_FILE = "appointments.json"

class ViewScheduleUI:
    def __init__(self, master, username, role):
        self.top = tk.Toplevel(master)
        self.top.configure(bg="#ffe4e1") 
        self.top.title("Xem lịch hẹn")
        self.top.geometry("800x500")
        self.username = username
        self.role = role

        self.appointments = load_data(APPOINTMENT_FILE)
        self.doctors = load_data("doctorsAcc.json")

        self.top.transient(master)
        self.top.grab_set()
        self.top.focus_set()

        self.create_schedule_view()

    def create_schedule_view(self):
        tk.Label(self.top, text="Danh sách lịch hẹn", font=("Helvetica", 14, "bold"), bg="#ffe4e1").pack(pady=10)

        if self.role == "Bệnh nhân":
            columns = ("Bệnh nhân", "Bác sĩ", "Chuyên khoa", "Ngày", "Giờ", "Trạng thái")
        else:
            columns = ("ID", "Bệnh nhân", "Bác sĩ", "Chuyên khoa", "Ngày", "Giờ", "Trạng thái")

        self.tree = ttk.Treeview(self.top, columns=columns, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if self.role != "Bệnh nhân":
            self.tree.heading("ID", text="ID")
            self.tree.column("ID", width=50)
            
        self.tree.heading("Bệnh nhân", text="Bệnh nhân")
        self.tree.heading("Bác sĩ", text="Bác sĩ")
        self.tree.heading("Chuyên khoa", text="Chuyên khoa")
        self.tree.heading("Ngày", text="Ngày")
        self.tree.heading("Giờ", text="Giờ")
        self.tree.heading("Trạng thái", text="Trạng thái")

        self.tree.column("Bệnh nhân", width=150)
        self.tree.column("Bác sĩ", width=150)
        self.tree.column("Chuyên khoa", width=120)
        self.tree.column("Ngày", width=100)
        self.tree.column("Giờ", width=80)
        self.tree.column("Trạng thái", width=100)

        scrollbar = ttk.Scrollbar(self.top, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.display_appointments()

        if self.role == "Bác sĩ":
            button_frame = tk.Frame(self.top, bg="#ffe4e1")
            button_frame.pack(pady=10)
            tk.Button(button_frame, text="Xác nhận", command=self.confirm_appointment, bg="#FF9999").pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Hủy", command=self.cancel_appointment, bg="#FF9999").pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Hoàn tất", command=self.complete_appointment, bg="#FF9999").pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="Xóa", command=self.delete_appointment, bg="#FF9999").pack(side=tk.LEFT, padx=5)

        tk.Button(self.top, text="Đóng", command=self.top.destroy, bg="#FF9999").pack(pady=10)

    def display_appointments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        doctor_appointments_count = 0

        for appointment in self.appointments:
            specialty = "Không xác định"
            for doctor in self.doctors:
                if doctor["id"] == appointment["doctor_id"]:
                    specialty = doctor.get("specialty", "Không xác định")
                    break

            if self.role == "Admin":
                self.tree.insert("", tk.END, values=(
                    appointment["appointment_id"],
                    appointment["patient_name"],
                    appointment["doctor_name"],
                    specialty,
                    appointment["date"],
                    appointment["time"],
                    appointment["status"]
                ))
            elif self.role == "Bác sĩ":
                for doctor in self.doctors:
                    if doctor["username"] == self.username and doctor["id"] == appointment["doctor_id"]:
                        self.tree.insert("", tk.END, values=(
                            appointment["appointment_id"],
                            appointment["patient_name"],
                            appointment["doctor_name"],
                            specialty,
                            appointment["date"],
                            appointment["time"],
                            appointment["status"]
                        ))
                        doctor_appointments_count += 1
            elif self.role == "Bệnh nhân":
                if appointment["patient_username"] == self.username:
                    self.tree.insert("", tk.END, values=(
                        appointment["patient_name"],
                        appointment["doctor_name"],
                        specialty,
                        appointment["date"],
                        appointment["time"],
                        appointment["status"]
                    ))
        if self.role == "Bác sĩ" and doctor_appointments_count == 0:
            messagebox.showinfo("Thông báo", "Hiện tại bạn không có lịch hẹn nào!")
            self.top.lift()

    def confirm_appointment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một lịch hẹn!")
            return

        appointment_id = int(self.tree.item(selected_item)["values"][0 if self.role != "Bệnh nhân" else -1])
        for appointment in self.appointments:
            if appointment["appointment_id"] == appointment_id:
                if appointment["status"] == "Chờ xác nhận":
                    appointment["status"] = "Đã xác nhận"
                    save_data(self.appointments, APPOINTMENT_FILE)
                    messagebox.showinfo("Thành công", "Lịch hẹn đã được xác nhận!")
                    self.display_appointments()
                else:
                    messagebox.showerror("Lỗi", "Lịch hẹn không ở trạng thái chờ xác nhận!")
                return

    def cancel_appointment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một lịch hẹn!")
            return

        appointment_id = int(self.tree.item(selected_item)["values"][0 if self.role != "Bệnh nhân" else -1])
        for appointment in self.appointments:
            if appointment["appointment_id"] == appointment_id:
                if appointment["status"] in ["Chờ xác nhận", "Đã xác nhận"]:
                    appointment["status"] = "Đã hủy"
                    save_data(self.appointments, APPOINTMENT_FILE)
                    messagebox.showinfo("Thành công", "Lịch hẹn đã bị hủy!")
                    self.display_appointments()
                else:
                    messagebox.showerror("Lỗi", "Lịch hẹn không thể hủy!")
                return

    def complete_appointment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một lịch hẹn!")
            return

        appointment_id = int(self.tree.item(selected_item)["values"][0 if self.role != "Bệnh nhân" else -1])
        for appointment in self.appointments:
            if appointment["appointment_id"] == appointment_id:
                if appointment["status"] == "Đã xác nhận":
                    appointment["status"] = "Hoàn tất"
                    save_data(self.appointments, APPOINTMENT_FILE)
                    messagebox.showinfo("Thành công", "Lịch hẹn đã được đánh dấu hoàn tất!")
                    self.display_appointments()
                else:
                    messagebox.showerror("Lỗi", "Lịch hẹn phải ở trạng thái xác nhận để hoàn tất!")
                return

    def delete_appointment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một lịch hẹn!")
            return

        appointment_id = int(self.tree.item(selected_item)["values"][0 if self.role != "Bệnh nhân" else -1])
        for i, appointment in enumerate(self.appointments):
            if appointment["appointment_id"] == appointment_id:
                if appointment["status"] in ["Đã hủy", "Hoàn tất"]:
                    self.appointments.pop(i)
                    save_data(self.appointments, APPOINTMENT_FILE)
                    messagebox.showinfo("Thành công", "Lịch hẹn đã được xóa!")
                    self.display_appointments()
                else:
                    messagebox.showerror("Lỗi", "Chỉ có thể xóa lịch hẹn ở trạng thái 'Đã hủy' hoặc 'Hoàn tất'!")
                return