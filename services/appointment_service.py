from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
import os
from models.appointment import Appointment, AppointmentStatus, AppointmentType
from models.dentist import Dentist

class AppointmentService:
    def __init__(self, data_file: str = "data/appointments.json"):
        self.data_file = data_file
        self.appointments = {}
        self._load_appointments()
        
    def _load_appointments(self):
        """Load appointments from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for appointment_data in data.values():
                        appointment = self._create_appointment_from_dict(appointment_data)
                        self.appointments[appointment.appointment_id] = appointment
            except Exception as e:
                print(f"Error loading appointments: {e}")
                
    def _save_appointments(self):
        """Save appointments to JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        try:
            with open(self.data_file, 'w') as f:
                json.dump({aid: appointment.to_dict() for aid, appointment in self.appointments.items()}, f, indent=2)
        except Exception as e:
            print(f"Error saving appointments: {e}")
            
    def _create_appointment_from_dict(self, data: Dict) -> Appointment:
        """Create an Appointment object from dictionary data"""
        appointment = Appointment(
            appointment_id=data['appointment_id'],
            patient_id=data['patient_id'],
            appointment_type=AppointmentType(data['appointment_type']),
            scheduled_date=datetime.fromisoformat(data['scheduled_date']),
            duration_minutes=data['duration_minutes'],
            dentist_id=data.get('dentist_id'),
            notes=data.get('notes', '')
        )
        
        # Restore additional data
        appointment.status = AppointmentStatus(data['status'])
        appointment.reminders_sent = data.get('reminders_sent', [])
        appointment.treatment_notes = data.get('treatment_notes', [])
        appointment.created_at = datetime.fromisoformat(data['created_at'])
        appointment.updated_at = datetime.fromisoformat(data['updated_at'])
        
        return appointment
        
    def create_appointment(self, patient_id: str, appointment_type: AppointmentType,
                          scheduled_date: datetime, duration_minutes: int = 60,
                          dentist_id: Optional[str] = None, notes: str = "") -> Optional[Appointment]:
        """Create a new appointment"""
        # Check for conflicts
        if self._has_conflict(scheduled_date, duration_minutes, dentist_id):
            return None
            
        appointment_id = f"A{len(self.appointments) + 1:04d}"
        appointment = Appointment(
            appointment_id=appointment_id,
            patient_id=patient_id,
            appointment_type=appointment_type,
            scheduled_date=scheduled_date,
            duration_minutes=duration_minutes,
            dentist_id=dentist_id,
            notes=notes
        )
        
        self.appointments[appointment_id] = appointment
        self._save_appointments()
        return appointment
        
    def _has_conflict(self, scheduled_date: datetime, duration_minutes: int, 
                     dentist_id: Optional[str] = None) -> bool:
        """Check if there's a scheduling conflict"""
        end_time = scheduled_date + timedelta(minutes=duration_minutes)
        
        for appointment in self.appointments.values():
            if appointment.status in [AppointmentStatus.CANCELLED, AppointmentStatus.NO_SHOW]:
                continue
                
            if dentist_id and appointment.dentist_id and appointment.dentist_id != dentist_id:
                continue
                
            appointment_end = appointment.get_end_time()
            if (scheduled_date < appointment_end and end_time > appointment.scheduled_date):
                return True
                
        return False
        
    def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        """Get appointment by ID"""
        return self.appointments.get(appointment_id)
        
    def get_appointments_by_patient(self, patient_id: str) -> List[Appointment]:
        """Get all appointments for a patient"""
        return [app for app in self.appointments.values() if app.patient_id == patient_id]
        
    def get_appointments_by_dentist(self, dentist_id: str) -> List[Appointment]:
        """Get all appointments for a dentist"""
        return [app for app in self.appointments.values() if app.dentist_id == dentist_id]
        
    def get_appointments_by_date(self, date: datetime) -> List[Appointment]:
        """Get appointments for a specific date"""
        return [app for app in self.appointments.values() 
                if app.scheduled_date.date() == date.date()]
        
    def get_appointments_by_status(self, status: AppointmentStatus) -> List[Appointment]:
        """Get appointments by status"""
        return [app for app in self.appointments.values() if app.status == status]
        
    def update_appointment_status(self, appointment_id: str, new_status: AppointmentStatus) -> bool:
        """Update appointment status"""
        appointment = self.get_appointment(appointment_id)
        if appointment:
            appointment.update_status(new_status)
            self._save_appointments()
            return True
        return False
        
    def cancel_appointment(self, appointment_id: str, reason: str = "") -> bool:
        """Cancel an appointment"""
        appointment = self.get_appointment(appointment_id)
        if appointment and appointment.can_be_cancelled():
            appointment.update_status(AppointmentStatus.CANCELLED)
            appointment.notes += f"\nCancelled: {reason}" if reason else "\nCancelled"
            self._save_appointments()
            return True
        return False
        
    def reschedule_appointment(self, appointment_id: str, new_date: datetime) -> bool:
        """Reschedule an appointment"""
        appointment = self.get_appointment(appointment_id)
        if not appointment:
            return False
            
        # Check for conflicts with new time
        if self._has_conflict(new_date, appointment.duration_minutes, appointment.dentist_id):
            return False
            
        appointment.scheduled_date = new_date
        appointment.updated_at = datetime.now()
        self._save_appointments()
        return True
        
    def get_available_slots(self, date: datetime, duration_minutes: int = 60,
                          dentist_id: Optional[str] = None) -> List[datetime]:
        """Get available appointment slots for a date"""
        # This would need to be integrated with dentist service for working hours
        # For now, return basic time slots
        slots = []
        start_time = datetime.combine(date.date(), datetime.min.time().replace(hour=9))
        end_time = datetime.combine(date.date(), datetime.min.time().replace(hour=17))
        
        current_time = start_time
        while current_time + timedelta(minutes=duration_minutes) <= end_time:
            if not self._has_conflict(current_time, duration_minutes, dentist_id):
                slots.append(current_time)
            current_time += timedelta(minutes=30)  # 30-minute intervals
            
        return slots
        
    def get_upcoming_appointments(self, hours: int = 24) -> List[Appointment]:
        """Get upcoming appointments within specified hours"""
        now = datetime.now()
        future_time = now + timedelta(hours=hours)
        
        return [app for app in self.appointments.values()
                if app.status in [AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED]
                and app.scheduled_date > now and app.scheduled_date <= future_time]
                
    def get_overdue_appointments(self) -> List[Appointment]:
        """Get appointments that are overdue"""
        now = datetime.now()
        return [app for app in self.appointments.values()
                if app.status in [AppointmentStatus.SCHEDULED, AppointmentStatus.CONFIRMED]
                and app.scheduled_date < now]
                
    def add_treatment_note(self, appointment_id: str, note: str, dentist_id: str) -> bool:
        """Add treatment note to appointment"""
        appointment = self.get_appointment(appointment_id)
        if appointment:
            appointment.add_treatment_note(note, dentist_id)
            self._save_appointments()
            return True
        return False
        
    def get_appointment_statistics(self) -> Dict:
        """Get appointment statistics"""
        total_appointments = len(self.appointments)
        status_counts = {}
        
        for status in AppointmentStatus:
            status_counts[status.value] = len(self.get_appointments_by_status(status))
            
        # Type distribution
        type_counts = {}
        for app_type in AppointmentType:
            type_counts[app_type.value] = len([app for app in self.appointments.values() 
                                             if app.appointment_type == app_type])
                                             
        return {
            "total_appointments": total_appointments,
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "upcoming_appointments": len(self.get_upcoming_appointments()),
            "overdue_appointments": len(self.get_overdue_appointments())
        }
