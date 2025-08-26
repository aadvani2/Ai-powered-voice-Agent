#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import speech_recognition as sr
import pyttsx3
import openai
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import threading
import queue

# Import API blueprints
from api.patient_api import patient_api
from api.appointment_api import appointment_api

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(patient_api)
app.register_blueprint(appointment_api)

# Initialize text-to-speech engine
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
except Exception as e:
    print(f"Warning: Could not initialize text-to-speech engine: {e}")
    engine = None

# Dental practice data
DENTAL_DATA = {
    "practice_name": "Bright Smile Dental Care",
    "address": "123 Main Street, Anytown, CA 90210",
    "phone": "(555) 123-4567",
    "hours": {
        "Monday": "8:00 AM - 6:00 PM",
        "Tuesday": "8:00 AM - 6:00 PM",
        "Wednesday": "8:00 AM - 6:00 PM",
        "Thursday": "8:00 AM - 6:00 PM",
        "Friday": "8:00 AM - 5:00 PM",
        "Saturday": "9:00 AM - 3:00 PM",
        "Sunday": "Closed"
    },
    "services": [
        "General Checkup",
        "Teeth Cleaning",
        "Cavity Filling",
        "Root Canal",
        "Teeth Whitening",
        "Dental Implants",
        "Emergency Care"
    ],
    "insurance": [
        "Delta Dental",
        "Aetna",
        "Cigna",
        "Blue Cross Blue Shield",
        "MetLife",
        "UnitedHealthcare"
    ]
}

# Available appointment slots (simplified for demo)
AVAILABLE_SLOTS = [
    "Monday 9:00 AM", "Monday 10:00 AM", "Monday 2:00 PM", "Monday 3:00 PM",
    "Tuesday 9:00 AM", "Tuesday 10:00 AM", "Tuesday 2:00 PM", "Tuesday 3:00 PM",
    "Wednesday 9:00 AM", "Wednesday 10:00 AM", "Wednesday 2:00 PM", "Wednesday 3:00 PM",
    "Thursday 9:00 AM", "Thursday 10:00 AM", "Thursday 2:00 PM", "Thursday 3:00 PM",
    "Friday 9:00 AM", "Friday 10:00 AM", "Friday 2:00 PM"
]

def get_ai_response(user_query):
    """Get AI response for dental queries"""
    try:
        system_prompt = f"""You are a helpful dental office assistant for {DENTAL_DATA['practice_name']}. 
        You help patients with appointment scheduling, insurance questions, and general dental inquiries.
        
        Practice Information:
        - Name: {DENTAL_DATA['practice_name']}
        - Address: {DENTAL_DATA['address']}
        - Phone: {DENTAL_DATA['phone']}
        - Hours: {json.dumps(DENTAL_DATA['hours'], indent=2)}
        - Services: {', '.join(DENTAL_DATA['services'])}
        - Accepted Insurance: {', '.join(DENTAL_DATA['insurance'])}
        - Available appointment slots: {', '.join(AVAILABLE_SLOTS)}
        
        Be friendly, professional, and helpful. If someone asks about appointments, offer available slots.
        If they ask about insurance, explain what we accept. Keep responses concise and natural for voice interaction."""
        
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        import traceback
        traceback.print_exc()
        return f"I'm sorry, I'm having trouble processing your request right now. Please try again or call us at {DENTAL_DATA['phone']}."

def speak_text(text):
    """Convert text to speech"""
    try:
        if engine:
            engine.say(text)
            engine.runAndWait()
        else:
            print(f"Text-to-speech not available: {text}")
    except Exception as e:
        print(f"Speech error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/voice-test')
def voice_test():
    return render_template('voice_test.html')

@app.route('/api/process-voice', methods=['POST'])
def process_voice():
    """Process voice input and return AI response"""
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Get AI response
        ai_response = get_ai_response(user_query)
        
        return jsonify({
            'response': ai_response,
            'practice_info': DENTAL_DATA
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/speak', methods=['POST'])
def speak():
    """Convert text to speech"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Run speech in a separate thread to avoid blocking
        threading.Thread(target=speak_text, args=(text,)).start()
        
        return jsonify({'status': 'Speaking started'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/appointment-slots')
def get_appointment_slots():
    """Get available appointment slots"""
    return jsonify({
        'slots': AVAILABLE_SLOTS,
        'practice_hours': DENTAL_DATA['hours']
    })

@app.route('/api/insurance-info')
def get_insurance_info():
    """Get insurance information"""
    return jsonify({
        'accepted_insurance': DENTAL_DATA['insurance'],
        'practice_info': {
            'name': DENTAL_DATA['practice_name'],
            'phone': DENTAL_DATA['phone']
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
