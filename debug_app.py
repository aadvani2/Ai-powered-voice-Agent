#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, get_ai_response
import os

# Test the function directly
print("Testing get_ai_response function...")
try:
    response = get_ai_response("I want to book an appointment")
    print(f"Response: {response}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test with Flask app context
print("\nTesting with Flask app context...")
with app.test_client() as client:
    response = client.post('/api/process-voice', 
                          json={'query': 'I want to book an appointment'})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
