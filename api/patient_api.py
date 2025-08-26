from flask import Blueprint, request, jsonify
from typing import Dict, List, Optional
from datetime import datetime
import json

from services.patient_service import PatientService

# Create Blueprint
patient_api = Blueprint('patient_api', __name__, url_prefix='/api/patients')

# Initialize service
patient_service = PatientService()

@patient_api.route('/', methods=['GET'])
def get_all_patients():
    """Get all patients with optional filtering"""
    try:
        # Get query parameters
        search = request.args.get('search', '')
        insurance_provider = request.args.get('insurance_provider', '')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get patients based on filters
        if search:
            patients = patient_service.search_patients(search)
        elif insurance_provider:
            patients = patient_service.get_patients_by_insurance(insurance_provider)
        else:
            patients = patient_service.get_all_patients()
            
        # Apply pagination
        total_count = len(patients)
        patients = patients[offset:offset + limit]
        
        # Convert to dictionaries
        patient_data = [patient.to_dict() for patient in patients]
        
        return jsonify({
            'success': True,
            'data': patient_data,
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

@patient_api.route('/<patient_id>', methods=['GET'])
def get_patient(patient_id: str):
    """Get a specific patient by ID"""
    try:
        patient = patient_service.get_patient(patient_id)
        
        if not patient:
            return jsonify({
                'success': False,
                'error': 'Patient not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': patient.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@patient_api.route('/', methods=['POST'])
def create_patient():
    """Create a new patient"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
                
        # Create patient
        patient = patient_service.create_patient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            date_of_birth=data['date_of_birth'],
            insurance_provider=data.get('insurance_provider'),
            insurance_id=data.get('insurance_id')
        )
        
        return jsonify({
            'success': True,
            'data': patient.to_dict(),
            'message': 'Patient created successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@patient_api.route('/<patient_id>', methods=['PUT'])
def update_patient(patient_id: str):
    """Update an existing patient"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided for update'
            }), 400
            
        # Update patient
        patient = patient_service.update_patient(patient_id, **data)
        
        if not patient:
            return jsonify({
                'success': False,
                'error': 'Patient not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': patient.to_dict(),
            'message': 'Patient updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@patient_api.route('/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id: str):
    """Delete a patient"""
    try:
        success = patient_service.delete_patient(patient_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Patient not found'
            }), 404
            
        return jsonify({
            'success': True,
            'message': 'Patient deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@patient_api.route('/search', methods=['GET'])
def search_patients():
    """Search patients by name, email, or phone"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
            
        patients = patient_service.search_patients(query)
        patient_data = [patient.to_dict() for patient in patients]
        
        return jsonify({
            'success': True,
            'data': patient_data,
            'count': len(patient_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@patient_api.route('/<patient_id>/medical-history', methods=['POST'])
def add_medical_history(patient_id: str):
    """Add medical history to a patient"""
    try:
        data = request.get_json()
        
        if not data or 'condition' not in data:
            return jsonify({
                'success': False,
                'error': 'Condition is required'
            }), 400
            
        patient_service.add_medical_history(
            patient_id=patient_id,
            condition=data['condition'],
            date=data.get('date', datetime.now().strftime('%Y-%m-%d')),
            notes=data.get('notes', '')
        )
        
        return jsonify({
            'success': True,
            'message': 'Medical history added successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@patient_api.route('/<patient_id>/treatments', methods=['POST'])
def add_treatment(patient_id: str):
    """Add treatment record to a patient"""
    try:
        data = request.get_json()
        
        required_fields = ['treatment_type', 'cost']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
                
        patient_service.add_treatment(
            patient_id=patient_id,
            treatment_type=data['treatment_type'],
            date=data.get('date', datetime.now().strftime('%Y-%m-%d')),
            cost=float(data['cost']),
            notes=data.get('notes', '')
        )
        
        return jsonify({
            'success': True,
            'message': 'Treatment record added successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@patient_api.route('/<patient_id>/notes', methods=['POST'])
def add_note(patient_id: str):
    """Add a note to a patient"""
    try:
        data = request.get_json()
        
        if not data or 'note' not in data:
            return jsonify({
                'success': False,
                'error': 'Note content is required'
            }), 400
            
        patient_service.add_note(
            patient_id=patient_id,
            note=data['note'],
            category=data.get('category', 'general')
        )
        
        return jsonify({
            'success': True,
            'message': 'Note added successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@patient_api.route('/statistics', methods=['GET'])
def get_patient_statistics():
    """Get patient statistics"""
    try:
        stats = patient_service.get_patient_statistics()
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@patient_api.route('/by-insurance/<provider>', methods=['GET'])
def get_patients_by_insurance(provider: str):
    """Get patients by insurance provider"""
    try:
        patients = patient_service.get_patients_by_insurance(provider)
        patient_data = [patient.to_dict() for patient in patients]
        
        return jsonify({
            'success': True,
            'data': patient_data,
            'count': len(patient_data),
            'insurance_provider': provider
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@patient_api.route('/lookup/email/<email>', methods=['GET'])
def lookup_patient_by_email(email: str):
    """Look up patient by email"""
    try:
        patient = patient_service.get_patient_by_email(email)
        
        if not patient:
            return jsonify({
                'success': False,
                'error': 'Patient not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': patient.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@patient_api.route('/lookup/phone/<phone>', methods=['GET'])
def lookup_patient_by_phone(phone: str):
    """Look up patient by phone number"""
    try:
        patient = patient_service.get_patient_by_phone(phone)
        
        if not patient:
            return jsonify({
                'success': False,
                'error': 'Patient not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': patient.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
