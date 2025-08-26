#!/usr/bin/env python3
"""
Database setup script for the dental voice agent
This script initializes the database with sample data
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.patient import Patient
from models.appointment import Appointment, AppointmentType, AppointmentStatus
from models.dentist import Dentist, DentistSpecialty
from models.billing import Invoice, BillingItem, PaymentMethod
from services.patient_service import PatientService
from services.appointment_service import AppointmentService
from services.billing_service import BillingService

def create_sample_patients() -> List[Patient]:
    """Create sample patient data"""
    patients = [
        {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john.smith@email.com',
            'phone': '(555) 123-4567',
            'date_of_birth': '1985-03-15',
            'insurance_provider': 'Delta Dental',
            'insurance_id': 'DD123456789'
        },
        {
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'email': 'sarah.johnson@email.com',
            'phone': '(555) 234-5678',
            'date_of_birth': '1990-07-22',
            'insurance_provider': 'Aetna',
            'insurance_id': 'AE987654321'
        },
        {
            'first_name': 'Michael',
            'last_name': 'Brown',
            'email': 'michael.brown@email.com',
            'phone': '(555) 345-6789',
            'date_of_birth': '1978-11-08',
            'insurance_provider': 'Cigna',
            'insurance_id': 'CG456789123'
        },
        {
            'first_name': 'Emily',
            'last_name': 'Davis',
            'email': 'emily.davis@email.com',
            'phone': '(555) 456-7890',
            'date_of_birth': '1992-05-14',
            'insurance_provider': 'Blue Cross Blue Shield',
            'insurance_id': 'BC789123456'
        },
        {
            'first_name': 'David',
            'last_name': 'Wilson',
            'email': 'david.wilson@email.com',
            'phone': '(555) 567-8901',
            'date_of_birth': '1983-09-30',
            'insurance_provider': None,
            'insurance_id': None
        }
    ]
    
    patient_service = PatientService()
    created_patients = []
    
    for patient_data in patients:
        patient = patient_service.create_patient(**patient_data)
        created_patients.append(patient)
        print(f"Created patient: {patient.get_full_name()}")
        
    return created_patients

def create_sample_appointments(patients: List[Patient]) -> List[Appointment]:
    """Create sample appointment data"""
    appointment_service = AppointmentService()
    created_appointments = []
    
    # Sample appointment data
    appointments_data = [
        {
            'patient': patients[0],
            'appointment_type': AppointmentType.CLEANING,
            'scheduled_date': datetime.now() + timedelta(days=2, hours=10),
            'duration_minutes': 45,
            'notes': 'Regular cleaning appointment'
        },
        {
            'patient': patients[1],
            'appointment_type': AppointmentType.CONSULTATION,
            'scheduled_date': datetime.now() + timedelta(days=3, hours=14),
            'duration_minutes': 60,
            'notes': 'Annual checkup'
        },
        {
            'patient': patients[2],
            'appointment_type': AppointmentType.FILLING,
            'scheduled_date': datetime.now() + timedelta(days=1, hours=9),
            'duration_minutes': 60,
            'notes': 'Cavity filling on tooth #14'
        },
        {
            'patient': patients[3],
            'appointment_type': AppointmentType.WHITENING,
            'scheduled_date': datetime.now() + timedelta(days=5, hours=11),
            'duration_minutes': 90,
            'notes': 'Teeth whitening treatment'
        },
        {
            'patient': patients[4],
            'appointment_type': AppointmentType.EMERGENCY,
            'scheduled_date': datetime.now() + timedelta(hours=2),
            'duration_minutes': 30,
            'notes': 'Emergency consultation - tooth pain'
        }
    ]
    
    for appt_data in appointments_data:
        appointment = appointment_service.create_appointment(
            patient_id=appt_data['patient'].patient_id,
            appointment_type=appt_data['appointment_type'],
            scheduled_date=appt_data['scheduled_date'],
            duration_minutes=appt_data['duration_minutes'],
            notes=appt_data['notes']
        )
        
        if appointment:
            created_appointments.append(appointment)
            print(f"Created appointment: {appointment.appointment_type.value} for {appt_data['patient'].get_full_name()}")
        else:
            print(f"Failed to create appointment for {appt_data['patient'].get_full_name()}")
            
    return created_appointments

def create_sample_invoices(patients: List[Patient], appointments: List[Appointment]) -> List[Invoice]:
    """Create sample invoice data"""
    billing_service = BillingService()
    created_invoices = []
    
    # Sample invoice data
    invoices_data = [
        {
            'patient': patients[0],
            'appointment': appointments[0] if len(appointments) > 0 else None,
            'items': [
                {'description': 'Teeth Cleaning', 'quantity': 1, 'unit_price': 120.00},
                {'description': 'X-Ray', 'quantity': 1, 'unit_price': 50.00}
            ]
        },
        {
            'patient': patients[1],
            'appointment': appointments[1] if len(appointments) > 1 else None,
            'items': [
                {'description': 'General Checkup', 'quantity': 1, 'unit_price': 150.00},
                {'description': 'Fluoride Treatment', 'quantity': 1, 'unit_price': 25.00}
            ]
        },
        {
            'patient': patients[2],
            'appointment': appointments[2] if len(appointments) > 2 else None,
            'items': [
                {'description': 'Cavity Filling', 'quantity': 1, 'unit_price': 200.00},
                {'description': 'Local Anesthesia', 'quantity': 1, 'unit_price': 30.00}
            ]
        }
    ]
    
    for invoice_data in invoices_data:
        # Create invoice
        invoice = billing_service.create_invoice(
            patient_id=invoice_data['patient'].patient_id,
            appointment_id=invoice_data['appointment'].appointment_id if invoice_data['appointment'] else None
        )
        
        # Add items
        for item_data in invoice_data['items']:
            billing_service.add_invoice_item(
                invoice_id=invoice.invoice_id,
                description=item_data['description'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price']
            )
            
        created_invoices.append(invoice)
        print(f"Created invoice: {invoice.invoice_id} for {invoice_data['patient'].get_full_name()}")
        
    return created_invoices

def add_sample_medical_history(patients: List[Patient]):
    """Add sample medical history to patients"""
    patient_service = PatientService()
    
    medical_history_data = [
        {
            'patient': patients[0],
            'conditions': [
                {'condition': 'Gingivitis', 'date': '2023-01-15', 'notes': 'Mild gum inflammation'},
                {'condition': 'Cavity', 'date': '2023-06-20', 'notes': 'Small cavity on tooth #12'}
            ]
        },
        {
            'patient': patients[1],
            'conditions': [
                {'condition': 'Sensitive Teeth', 'date': '2023-03-10', 'notes': 'Cold sensitivity'},
                {'condition': 'Wisdom Tooth Pain', 'date': '2023-08-05', 'notes': 'Impacted wisdom tooth'}
            ]
        },
        {
            'patient': patients[2],
            'conditions': [
                {'condition': 'Root Canal', 'date': '2022-11-12', 'notes': 'Root canal on tooth #19'},
                {'condition': 'Crown Placement', 'date': '2023-02-28', 'notes': 'Crown on tooth #19'}
            ]
        }
    ]
    
    for history_data in medical_history_data:
        for condition in history_data['conditions']:
            patient_service.add_medical_history(
                patient_id=history_data['patient'].patient_id,
                condition=condition['condition'],
                date=condition['date'],
                notes=condition['notes']
            )
        print(f"Added medical history for {history_data['patient'].get_full_name()}")

def add_sample_treatments(patients: List[Patient]):
    """Add sample treatment records to patients"""
    patient_service = PatientService()
    
    treatments_data = [
        {
            'patient': patients[0],
            'treatments': [
                {'treatment_type': 'Teeth Cleaning', 'date': '2023-01-15', 'cost': 120.00, 'notes': 'Regular cleaning'},
                {'treatment_type': 'Cavity Filling', 'date': '2023-06-20', 'cost': 200.00, 'notes': 'Filling on tooth #12'}
            ]
        },
        {
            'patient': patients[1],
            'treatments': [
                {'treatment_type': 'General Checkup', 'date': '2023-03-10', 'cost': 150.00, 'notes': 'Annual checkup'},
                {'treatment_type': 'Wisdom Tooth Extraction', 'date': '2023-08-05', 'cost': 500.00, 'notes': 'Surgical extraction'}
            ]
        },
        {
            'patient': patients[2],
            'treatments': [
                {'treatment_type': 'Root Canal', 'date': '2022-11-12', 'cost': 800.00, 'notes': 'Root canal on tooth #19'},
                {'treatment_type': 'Crown Placement', 'date': '2023-02-28', 'cost': 1200.00, 'notes': 'Porcelain crown'}
            ]
        }
    ]
    
    for treatment_data in treatments_data:
        for treatment in treatment_data['treatments']:
            patient_service.add_treatment(
                patient_id=treatment_data['patient'].patient_id,
                treatment_type=treatment['treatment_type'],
                date=treatment['date'],
                cost=treatment['cost'],
                notes=treatment['notes']
            )
        print(f"Added treatment records for {treatment_data['patient'].get_full_name()}")

def add_sample_notes(patients: List[Patient]):
    """Add sample notes to patients"""
    patient_service = PatientService()
    
    notes_data = [
        {
            'patient': patients[0],
            'notes': [
                {'note': 'Patient prefers morning appointments', 'category': 'preference'},
                {'note': 'Allergic to penicillin', 'category': 'medical'},
                {'note': 'Excellent oral hygiene habits', 'category': 'general'}
            ]
        },
        {
            'patient': patients[1],
            'notes': [
                {'note': 'Anxious about dental procedures', 'category': 'behavioral'},
                {'note': 'Prefers female dentists', 'category': 'preference'},
                {'note': 'Has dental insurance through employer', 'category': 'insurance'}
            ]
        },
        {
            'patient': patients[2],
            'notes': [
                {'note': 'History of dental anxiety', 'category': 'behavioral'},
                {'note': 'Requires sedation for major procedures', 'category': 'medical'},
                {'note': 'Has flexible schedule for appointments', 'category': 'preference'}
            ]
        }
    ]
    
    for note_data in notes_data:
        for note in note_data['notes']:
            patient_service.add_note(
                patient_id=note_data['patient'].patient_id,
                note=note['note'],
                category=note['category']
            )
        print(f"Added notes for {note_data['patient'].get_full_name()}")

def main():
    """Main setup function"""
    print("🚀 Setting up Dental Voice Agent Database...")
    print("=" * 50)
    
    try:
        # Create sample patients
        print("\n📋 Creating sample patients...")
        patients = create_sample_patients()
        
        # Create sample appointments
        print("\n📅 Creating sample appointments...")
        appointments = create_sample_appointments(patients)
        
        # Create sample invoices
        print("\n💰 Creating sample invoices...")
        invoices = create_sample_invoices(patients, appointments)
        
        # Add sample medical history
        print("\n🏥 Adding sample medical history...")
        add_sample_medical_history(patients)
        
        # Add sample treatments
        print("\n🦷 Adding sample treatment records...")
        add_sample_treatments(patients)
        
        # Add sample notes
        print("\n📝 Adding sample patient notes...")
        add_sample_notes(patients)
        
        print("\n" + "=" * 50)
        print("✅ Database setup completed successfully!")
        print(f"📊 Created {len(patients)} patients")
        print(f"📅 Created {len(appointments)} appointments")
        print(f"💰 Created {len(invoices)} invoices")
        print("\n🎉 Your dental voice agent is ready to use!")
        
    except Exception as e:
        print(f"\n❌ Error during database setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
