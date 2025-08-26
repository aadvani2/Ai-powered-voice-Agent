from datetime import datetime, timedelta
from typing import Optional, List, Dict
from enum import Enum

class AppointmentStatus(Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class AppointmentType(Enum):
    CONSULTATION = "consultation"
    CLEANING = "cleaning"
    FILLING = "filling"
    ROOT_CANAL = "root_canal"
    EXTRACTION = "extraction"
    WHITENING = "whitening"
    IMPLANT = "implant"
    EMERGENCY = "emergency"
    FOLLOW_UP = "follow_up"

class Appointment:
    def __init__(self, appointment_id: str, patient_id: str, appointment_type: AppointmentType,
                 scheduled_date: datetime, duration_minutes: int = 60,
                 dentist_id: Optional[str] = None, notes: str = ""):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.appointment_type = appointment_type
        self.scheduled_date = scheduled_date
        self.duration_minutes = duration_minutes
        self.dentist_id = dentist_id
        self.notes = notes
        self.status = AppointmentStatus.SCHEDULED
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.reminders_sent = []
        self.treatment_notes = []
        
    def to_dict(self) -> Dict:
        return {
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'appointment_type': self.appointment_type.value,
            'scheduled_date': self.scheduled_date.isoformat(),
            'duration_minutes': self.duration_minutes,
            'dentist_id': self.dentist_id,
            'notes': self.notes,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'reminders_sent': self.reminders_sent,
            'treatment_notes': self.treatment_notes
        }
    
    def update_status(self, new_status: AppointmentStatus):
        self.status = new_status
        self.updated_at = datetime.now()
    
    def add_treatment_note(self, note: str, dentist_id: str):
        self.treatment_notes.append({
            'note': note,
            'dentist_id': dentist_id,
            'timestamp': datetime.now().isoformat()
        })
        self.updated_at = datetime.now()
    
    def add_reminder_sent(self, reminder_type: str):
        self.reminders_sent.append({
            'type': reminder_type,
            'sent_at': datetime.now().isoformat()
        })
    
    def get_end_time(self) -> datetime:
        return self.scheduled_date + timedelta(minutes=self.duration_minutes)
    
    def is_conflict_with(self, other_appointment) -> bool:
        if self.scheduled_date < other_appointment.get_end_time() and \
           self.get_end_time() > other_appointment.scheduled_date:
            return True
        return False
    
    def is_upcoming(self, hours: int = 24) -> bool:
        now = datetime.now()
        future_time = now + timedelta(hours=hours)
        return self.scheduled_date > now and self.scheduled_date <= future_time
    
    def can_be_cancelled(self) -> bool:
        # Can cancel if more than 24 hours before appointment
        return self.scheduled_date > datetime.now() + timedelta(hours=24)
