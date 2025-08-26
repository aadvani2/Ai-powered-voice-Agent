from typing import List, Dict, Optional
from datetime import datetime
import json
import os
from models.patient import Patient

class PatientService:
    def __init__(self, data_file: str = "data/patients.json"):
        self.data_file = data_file
        self.patients = {}
        self._load_patients()
        
    def _load_patients(self):
        """Load patients from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for patient_data in data.values():
                        patient = self._create_patient_from_dict(patient_data)
                        self.patients[patient.patient_id] = patient
            except Exception as e:
                print(f"Error loading patients: {e}")
                
    def _save_patients(self):
        """Save patients to JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        try:
            with open(self.data_file, 'w') as f:
                json.dump({pid: patient.to_dict() for pid, patient in self.patients.items()}, f, indent=2)
        except Exception as e:
            print(f"Error saving patients: {e}")
            
    def _create_patient_from_dict(self, data: Dict) -> Patient:
        """Create a Patient object from dictionary data"""
        patient = Patient(
            patient_id=data['patient_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            date_of_birth=data['date_of_birth'],
            insurance_provider=data.get('insurance_provider'),
            insurance_id=data.get('insurance_id')
        )
        
        # Restore additional data
        patient.medical_history = data.get('medical_history', [])
        patient.appointments = data.get('appointments', [])
        patient.treatments = data.get('treatments', [])
        patient.notes = data.get('notes', [])
        patient.created_at = datetime.fromisoformat(data['created_at'])
        patient.updated_at = datetime.fromisoformat(data['updated_at'])
        
        return patient
        
    def create_patient(self, first_name: str, last_name: str, email: str, phone: str,
                      date_of_birth: str, insurance_provider: Optional[str] = None,
                      insurance_id: Optional[str] = None) -> Patient:
        """Create a new patient"""
        patient_id = f"P{len(self.patients) + 1:04d}"
        patient = Patient(
            patient_id=patient_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            insurance_provider=insurance_provider,
            insurance_id=insurance_id
        )
        
        self.patients[patient_id] = patient
        self._save_patients()
        return patient
        
    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """Get patient by ID"""
        return self.patients.get(patient_id)
        
    def get_patient_by_email(self, email: str) -> Optional[Patient]:
        """Get patient by email"""
        for patient in self.patients.values():
            if patient.email.lower() == email.lower():
                return patient
        return None
        
    def get_patient_by_phone(self, phone: str) -> Optional[Patient]:
        """Get patient by phone number"""
        for patient in self.patients.values():
            if patient.phone == phone:
                return patient
        return None
        
    def search_patients(self, query: str) -> List[Patient]:
        """Search patients by name, email, or phone"""
        query = query.lower()
        results = []
        
        for patient in self.patients.values():
            if (query in patient.first_name.lower() or 
                query in patient.last_name.lower() or
                query in patient.get_full_name().lower() or
                query in patient.email.lower() or
                query in patient.phone):
                results.append(patient)
                
        return results
        
    def update_patient(self, patient_id: str, **kwargs) -> Optional[Patient]:
        """Update patient information"""
        patient = self.get_patient(patient_id)
        if not patient:
            return None
            
        for key, value in kwargs.items():
            if hasattr(patient, key):
                setattr(patient, key, value)
                
        patient.updated_at = datetime.now()
        self._save_patients()
        return patient
        
    def delete_patient(self, patient_id: str) -> bool:
        """Delete a patient"""
        if patient_id in self.patients:
            del self.patients[patient_id]
            self._save_patients()
            return True
        return False
        
    def get_all_patients(self) -> List[Patient]:
        """Get all patients"""
        return list(self.patients.values())
        
    def get_patients_by_insurance(self, insurance_provider: str) -> List[Patient]:
        """Get patients by insurance provider"""
        return [p for p in self.patients.values() 
                if p.insurance_provider and p.insurance_provider.lower() == insurance_provider.lower()]
                
    def get_patients_with_overdue_appointments(self) -> List[Patient]:
        """Get patients with overdue appointments"""
        # This would need to be implemented with appointment service integration
        return []
        
    def add_medical_history(self, patient_id: str, condition: str, date: str, notes: str = ""):
        """Add medical history to patient"""
        patient = self.get_patient(patient_id)
        if patient:
            patient.add_medical_history(condition, date, notes)
            self._save_patients()
            
    def add_treatment(self, patient_id: str, treatment_type: str, date: str, cost: float, notes: str = ""):
        """Add treatment record to patient"""
        patient = self.get_patient(patient_id)
        if patient:
            patient.add_treatment(treatment_type, date, cost, notes)
            self._save_patients()
            
    def add_note(self, patient_id: str, note: str, category: str = "general"):
        """Add note to patient"""
        patient = self.get_patient(patient_id)
        if patient:
            patient.add_note(note, category)
            self._save_patients()
            
    def get_patient_statistics(self) -> Dict:
        """Get patient statistics"""
        total_patients = len(self.patients)
        patients_with_insurance = len([p for p in self.patients.values() if p.insurance_provider])
        
        # Age distribution
        age_groups = {"0-17": 0, "18-30": 0, "31-50": 0, "51-70": 0, "70+": 0}
        for patient in self.patients.values():
            age = patient.get_age()
            if age < 18:
                age_groups["0-17"] += 1
            elif age < 31:
                age_groups["18-30"] += 1
            elif age < 51:
                age_groups["31-50"] += 1
            elif age < 71:
                age_groups["51-70"] += 1
            else:
                age_groups["70+"] += 1
                
        return {
            "total_patients": total_patients,
            "patients_with_insurance": patients_with_insurance,
            "insurance_coverage_percentage": (patients_with_insurance / total_patients * 100) if total_patients > 0 else 0,
            "age_distribution": age_groups
        }
