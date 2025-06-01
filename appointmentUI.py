import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from utils import load_data, save_data
from model import Appointment
from datetime import datetime

APPOINTMENT_FILE = "appointments.json"

class AppointmentUI:
    def __init__(self, master, username):
        self.top = tk.Toplevel(master)
        self.top.configure(bg="#ffe4e1") 
        self.top.title("Đặt lịch khám")
        self.top.geometry("400x400")
        self.username = username

        self.top.transient(master)
        self.top.grab_set()  
        self.top.focus_set()

        doctors = load_data("doctorsAcc.json")
        # Tạo danh sách hiển thị và ánh xạ tên hiển thị đến đối tượng bác sĩ
        self.doctor_names = []
        self.doctor_map = {}

        for doctor in doctors:
            display_name = f"{doctor['name']} - {doctor['specialty']}"
            self.doctor_names.append(display_name)
            self.doctor_map[display_name] = doctor  

        # Giao diện chọn bác sĩ
        tk.Label(self.top, text="Chọn bác sĩ:", bg="#ffe4e1").pack(pady=5)
        self.doctor_combobox = ttk.Combobox(self.top, values=self.doctor_names, state="readonly", width=40)
        self.doctor_combobox.pack(pady=5)

        # Giao diện nhập thông tin bệnh nhân
        tk.Label(self.top, text="Họ và tên bệnh nhân:", bg="#ffe4e1").pack(pady=5)
        self.patient_name_entry = tk.Entry(self.top)
        self.patient_name_entry.pack(pady=5)

        tk.Label(self.top, text="Số điện thoại:", bg="#ffe4e1").pack(pady=5)
        self.phone_entry = tk.Entry(self.top)
        self.phone_entry.pack(pady=5)

        tk.Label(self.top, text="Ngày (DD/MM/YYYY):", bg="#ffe4e1").pack(pady=5)
        self.date_entry = tk.Entry(self.top)
        self.date_entry.pack(pady=5)

        tk.Label(self.top, text="Khung giờ khám:", bg="#ffe4e1").pack(pady=5)
        def generate_time_slots():
            slots = []
            for hour in range(7, 20):  
                time_str = f"{hour:02d}:30"
                slots.append(time_str)
            return slots
        time_slots = generate_time_slots()
        self.time_combobox = ttk.Combobox(self.top, values=time_slots, state="readonly")
        self.time_combobox.pack(pady=5)

        tk.Button(self.top, text="Xác nhận", command=self.confirm_appointment,bg="#FF9999", width=20).pack(pady=20)

    def confirm_appointment(self):
        display_name = self.doctor_combobox.get()
        patient_name = self.patient_name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        date = self.date_entry.get().strip()
        time = self.time_combobox.get()

        # Kiểm tra xem các trường có bị bỏ trống hay không
        if not all([display_name, patient_name, phone, date, time]):
            messagebox.showwarning("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        
        try:
            date_obj = datetime.strptime(date, "%d/%m/%Y")
            if date_obj < datetime.now():
                messagebox.showerror("Lỗi", "Ngày hẹn phải là ngày trong tương lai!")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Ngày không hợp lệ. Định dạng đúng là DD/MM/YYYY.")
            return

        # Kiểm tra định dạng số điện thoại
        if not phone.isdigit() or len(phone) < 10:
            messagebox.showerror("Lỗi", "Số điện thoại phải là số và có ít nhất 10 chữ số!")
            return

        # Lấy thông tin bác sĩ từ doctor_map
        doctor = self.doctor_map.get(display_name)
        if not doctor:
            messagebox.showerror("Lỗi", "Vui lòng chọn bác sĩ hợp lệ!")
            return

        doctor_id = doctor["id"]
        doctor_name = doctor["name"]

        # Kiểm tra trùng lịch hẹn
        appointments = load_data(APPOINTMENT_FILE)
        for appointment in appointments:
            if appointment["doctor_id"] == doctor_id and appointment["date"] == date and appointment["time"] == time:
                messagebox.showerror("Lỗi", "Bác sĩ đã có lịch hẹn vào thời điểm này!")
                return

        # Tạo ID cho lịch hẹn
        appointment_id = len(appointments) + 1

        # Tạo đối tượng Appointment
        appointment = Appointment(
            appointment_id=appointment_id,
            patient_username=self.username,
            patient_name=patient_name,
            doctor_id=doctor_id,
            doctor_name=doctor_name,
            date=date,
            time=time,
            status="Chờ xác nhận"
        )

        # Lưu lịch hẹn vào file appointments.json
        appointments.append(appointment.to_dict())
        save_data(appointments, APPOINTMENT_FILE)

        messagebox.showinfo("Thành công", "Đặt lịch hẹn thành công!")
        self.top.destroy()