class Doctor:
    def __init__(self, id, username, password, name, specialty, email):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.specialty = specialty
        self.email = email
    
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "specialty": self.specialty,
            "email": self.email
        }

    @staticmethod
    def from_dict(data):
        return Doctor(
            data.get("id", ""),
            data.get("username", ""),
            data["password"],
            data["name"],
            data["specialty"],
            data["email"]
        )

class Appointment:
    def __init__(self, appointment_id, patient_username, patient_name, doctor_id, doctor_name, date, time, status="Chờ xác nhận"):
        self.appointment_id = appointment_id
        self.patient_username = patient_username
        self.patient_name = patient_name
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name
        self.date = date
        self.time = time  
        self.status = status

    def to_dict(self):
        return self.__dict__