from flask import Blueprint, request, jsonify
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

from services.appointment_service import AppointmentService
from models.appointment import AppointmentType, AppointmentStatus

# Create Blueprint
appointment_api = Blueprint('appointment_api', __name__, url_prefix='/api/appointments')

# Initialize service
appointment_service = AppointmentService()

@appointment_api.route('/', methods=['GET'])
def get_all_appointments():
    """Get all appointments with optional filtering"""
    try:
        # Get query parameters
        patient_id = request.args.get('patient_id', '')
        dentist_id = request.args.get('dentist_id', '')
        status = request.args.get('status', '')
        date = request.args.get('date', '')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get appointments based on filters
        if patient_id:
            appointments = appointment_service.get_appointments_by_patient(patient_id)
        elif dentist_id:
            appointments = appointment_service.get_appointments_by_dentist(dentist_id)
        elif status:
            try:
                status_enum = AppointmentStatus(status)
                appointments = appointment_service.get_appointments_by_status(status_enum)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid status value'
                }), 400
        elif date:
            try:
                date_obj = datetime.fromisoformat(date)
                appointments = appointment_service.get_appointments_by_date(date_obj)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid date format. Use YYYY-MM-DD'
                }), 400
        else:
            appointments = list(appointment_service.appointments.values())
            
        # Apply pagination
        total_count = len(appointments)
        appointments = appointments[offset:offset + limit]
        
        # Convert to dictionaries
        appointment_data = [appointment.to_dict() for appointment in appointments]
        
        return jsonify({
            'success': True,
            'data': appointment_data,
            'pagination': {
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'has_more': offset + limit < total_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id: str):
    """Get a specific appointment by ID"""
    try:
        appointment = appointment_service.get_appointment(appointment_id)
        
        if not appointment:
            return jsonify({
                'success': False,
                'error': 'Appointment not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': appointment.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/', methods=['POST'])
def create_appointment():
    """Create a new appointment"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patient_id', 'appointment_type', 'scheduled_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
                
        # Parse appointment type
        try:
            appointment_type = AppointmentType(data['appointment_type'])
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid appointment type'
            }), 400
            
        # Parse scheduled date
        try:
            scheduled_date = datetime.fromisoformat(data['scheduled_date'])
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
            }), 400
            
        # Create appointment
        appointment = appointment_service.create_appointment(
            patient_id=data['patient_id'],
            appointment_type=appointment_type,
            scheduled_date=scheduled_date,
            duration_minutes=data.get('duration_minutes', 60),
            dentist_id=data.get('dentist_id'),
            notes=data.get('notes', '')
        )
        
        if not appointment:
            return jsonify({
                'success': False,
                'error': 'Appointment could not be created. Time slot may be unavailable.'
            }), 409
            
        return jsonify({
            'success': True,
            'data': appointment.to_dict(),
            'message': 'Appointment created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/<appointment_id>', methods=['PUT'])
def update_appointment(appointment_id: str):
    """Update an existing appointment"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided for update'
            }), 400
            
        # Handle status updates
        if 'status' in data:
            try:
                new_status = AppointmentStatus(data['status'])
                success = appointment_service.update_appointment_status(appointment_id, new_status)
                if not success:
                    return jsonify({
                        'success': False,
                        'error': 'Appointment not found'
                    }), 404
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid status value'
                }), 400
                
        # Handle rescheduling
        if 'scheduled_date' in data:
            try:
                new_date = datetime.fromisoformat(data['scheduled_date'])
                success = appointment_service.reschedule_appointment(appointment_id, new_date)
                if not success:
                    return jsonify({
                        'success': False,
                        'error': 'Appointment could not be rescheduled. Time slot may be unavailable.'
                    }), 409
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)'
                }), 400
                
        # Get updated appointment
        appointment = appointment_service.get_appointment(appointment_id)
        
        return jsonify({
            'success': True,
            'data': appointment.to_dict(),
            'message': 'Appointment updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/<appointment_id>', methods=['DELETE'])
def cancel_appointment(appointment_id: str):
    """Cancel an appointment"""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', '')
        
        success = appointment_service.cancel_appointment(appointment_id, reason)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Appointment not found or cannot be cancelled'
            }), 404
            
        return jsonify({
            'success': True,
            'message': 'Appointment cancelled successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/available-slots', methods=['GET'])
def get_available_slots():
    """Get available appointment slots"""
    try:
        date_str = request.args.get('date', '')
        duration = request.args.get('duration', 60, type=int)
        dentist_id = request.args.get('dentist_id', '')
        
        if not date_str:
            return jsonify({
                'success': False,
                'error': 'Date parameter is required'
            }), 400
            
        try:
            date = datetime.fromisoformat(date_str)
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }), 400
            
        slots = appointment_service.get_available_slots(date, duration, dentist_id)
        slot_data = [slot.isoformat() for slot in slots]
        
        return jsonify({
            'success': True,
            'data': {
                'date': date_str,
                'duration_minutes': duration,
                'available_slots': slot_data,
                'count': len(slot_data)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/upcoming', methods=['GET'])
def get_upcoming_appointments():
    """Get upcoming appointments"""
    try:
        hours = request.args.get('hours', 24, type=int)
        
        appointments = appointment_service.get_upcoming_appointments(hours)
        appointment_data = [appointment.to_dict() for appointment in appointments]
        
        return jsonify({
            'success': True,
            'data': appointment_data,
            'count': len(appointment_data),
            'hours_ahead': hours
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/overdue', methods=['GET'])
def get_overdue_appointments():
    """Get overdue appointments"""
    try:
        appointments = appointment_service.get_overdue_appointments()
        appointment_data = [appointment.to_dict() for appointment in appointments]
        
        return jsonify({
            'success': True,
            'data': appointment_data,
            'count': len(appointment_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/<appointment_id>/treatment-notes', methods=['POST'])
def add_treatment_note(appointment_id: str):
    """Add treatment note to an appointment"""
    try:
        data = request.get_json()
        
        if not data or 'note' not in data or 'dentist_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Note and dentist_id are required'
            }), 400
            
        success = appointment_service.add_treatment_note(
            appointment_id=appointment_id,
            note=data['note'],
            dentist_id=data['dentist_id']
        )
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Appointment not found'
            }), 404
            
        return jsonify({
            'success': True,
            'message': 'Treatment note added successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/statistics', methods=['GET'])
def get_appointment_statistics():
    """Get appointment statistics"""
    try:
        stats = appointment_service.get_appointment_statistics()
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/by-patient/<patient_id>', methods=['GET'])
def get_patient_appointments(patient_id: str):
    """Get all appointments for a specific patient"""
    try:
        appointments = appointment_service.get_appointments_by_patient(patient_id)
        appointment_data = [appointment.to_dict() for appointment in appointments]
        
        return jsonify({
            'success': True,
            'data': appointment_data,
            'count': len(appointment_data),
            'patient_id': patient_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/by-dentist/<dentist_id>', methods=['GET'])
def get_dentist_appointments(dentist_id: str):
    """Get all appointments for a specific dentist"""
    try:
        appointments = appointment_service.get_appointments_by_dentist(dentist_id)
        appointment_data = [appointment.to_dict() for appointment in appointments]
        
        return jsonify({
            'success': True,
            'data': appointment_data,
            'count': len(appointment_data),
            'dentist_id': dentist_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/by-date/<date>', methods=['GET'])
def get_appointments_by_date(date: str):
    """Get appointments for a specific date"""
    try:
        try:
            date_obj = datetime.fromisoformat(date)
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }), 400
            
        appointments = appointment_service.get_appointments_by_date(date_obj)
        appointment_data = [appointment.to_dict() for appointment in appointments]
        
        return jsonify({
            'success': True,
            'data': appointment_data,
            'count': len(appointment_data),
            'date': date
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/types', methods=['GET'])
def get_appointment_types():
    """Get all available appointment types"""
    try:
        types = [app_type.value for app_type in AppointmentType]
        
        return jsonify({
            'success': True,
            'data': types
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@appointment_api.route('/statuses', methods=['GET'])
def get_appointment_statuses():
    """Get all available appointment statuses"""
    try:
        statuses = [status.value for status in AppointmentStatus]
        
        return jsonify({
            'success': True,
            'data': statuses
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
