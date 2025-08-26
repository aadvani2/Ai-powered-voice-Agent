from datetime import datetime, time
from typing import List, Dict, Optional
from enum import Enum

class DentistSpecialty(Enum):
    GENERAL = "general"
    ORTHODONTIST = "orthodontist"
    ENDODONTIST = "endodontist"
    PERIODONTIST = "periodontist"
    ORAL_SURGEON = "oral_surgeon"
    PEDIATRIC = "pediatric"
    COSMETIC = "cosmetic"

class Dentist:
    def __init__(self, dentist_id: str, first_name: str, last_name: str,
                 email: str, phone: str, specialty: DentistSpecialty,
                 license_number: str, years_experience: int = 0):
        self.dentist_id = dentist_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.specialty = specialty
        self.license_number = license_number
        self.years_experience = years_experience
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.working_hours = {
            'monday': {'start': time(9, 0), 'end': time(17, 0)},
            'tuesday': {'start': time(9, 0), 'end': time(17, 0)},
            'wednesday': {'start': time(9, 0), 'end': time(17, 0)},
            'thursday': {'start': time(9, 0), 'end': time(17, 0)},
            'friday': {'start': time(9, 0), 'end': time(16, 0)},
            'saturday': {'start': time(9, 0), 'end': time(15, 0)},
            'sunday': None
        }
        self.vacation_dates = []
        self.appointments = []
        self.notes = []
        
    def to_dict(self) -> Dict:
        return {
            'dentist_id': self.dentist_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'specialty': self.specialty.value,
            'license_number': self.license_number,
            'years_experience': self.years_experience,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'working_hours': {day: {'start': hours['start'].isoformat(), 'end': hours['end'].isoformat()} if hours else None 
                             for day, hours in self.working_hours.items()},
            'vacation_dates': self.vacation_dates,
            'appointments': self.appointments,
            'notes': self.notes
        }
    
    def get_full_name(self) -> str:
        return f"Dr. {self.first_name} {self.last_name}"
    
    def set_working_hours(self, day: str, start_time: time, end_time: time):
        if day.lower() in self.working_hours:
            self.working_hours[day.lower()] = {'start': start_time, 'end': end_time}
            self.updated_at = datetime.now()
    
    def add_vacation_date(self, start_date: datetime, end_date: datetime, reason: str = ""):
        self.vacation_dates.append({
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'reason': reason,
            'added_at': datetime.now().isoformat()
        })
        self.updated_at = datetime.now()
    
    def is_available_on_date(self, date: datetime) -> bool:
        # Check if it's a vacation day
        for vacation in self.vacation_dates:
            vacation_start = datetime.fromisoformat(vacation['start_date'])
            vacation_end = datetime.fromisoformat(vacation['end_date'])
            if vacation_start <= date <= vacation_end:
                return False
        
        # Check working hours
        day_name = date.strftime('%A').lower()
        if day_name not in self.working_hours or self.working_hours[day_name] is None:
            return False
        
        working_hours = self.working_hours[day_name]
        appointment_time = date.time()
        return working_hours['start'] <= appointment_time <= working_hours['end']
    
    def add_note(self, note: str, category: str = "general"):
        self.notes.append({
            'note': note,
            'category': category,
            'added_at': datetime.now().isoformat()
        })
        self.updated_at = datetime.now()
    
    def get_available_slots(self, date: datetime, duration_minutes: int = 60) -> List[datetime]:
        if not self.is_available_on_date(date):
            return []
        
        day_name = date.strftime('%A').lower()
        working_hours = self.working_hours[day_name]
        
        slots = []
        current_time = working_hours['start']
        
        while current_time <= working_hours['end']:
            slot_datetime = datetime.combine(date.date(), current_time)
            slots.append(slot_datetime)
            # Add duration_minutes to current_time
            current_time = (datetime.combine(date.date(), current_time) + 
                          datetime.timedelta(minutes=duration_minutes)).time()
        
        return slots
