from datetime import datetime
from typing import Optional, List, Dict
import json

class Patient:
    def __init__(self, patient_id: str, first_name: str, last_name: str, 
                 email: str, phone: str, date_of_birth: str, 
                 insurance_provider: Optional[str] = None,
                 insurance_id: Optional[str] = None):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.date_of_birth = date_of_birth
        self.insurance_provider = insurance_provider
        self.insurance_id = insurance_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.medical_history = []
        self.appointments = []
        self.treatments = []
        self.notes = []
        
    def to_dict(self) -> Dict:
        return {
            'patient_id': self.patient_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth,
            'insurance_provider': self.insurance_provider,
            'insurance_id': self.insurance_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'medical_history': self.medical_history,
            'appointments': self.appointments,
            'treatments': self.treatments,
            'notes': self.notes
        }
    
    def add_medical_history(self, condition: str, date: str, notes: str = ""):
        self.medical_history.append({
            'condition': condition,
            'date': date,
            'notes': notes,
            'added_at': datetime.now().isoformat()
        })
        self.updated_at = datetime.now()
    
    def add_treatment(self, treatment_type: str, date: str, cost: float, notes: str = ""):
        self.treatments.append({
            'treatment_type': treatment_type,
            'date': date,
            'cost': cost,
            'notes': notes,
            'added_at': datetime.now().isoformat()
        })
        self.updated_at = datetime.now()
    
    def add_note(self, note: str, category: str = "general"):
        self.notes.append({
            'note': note,
            'category': category,
            'added_at': datetime.now().isoformat()
        })
        self.updated_at = datetime.now()
    
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self) -> int:
        birth_date = datetime.strptime(self.date_of_birth, "%Y-%m-%d")
        today = datetime.now()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
