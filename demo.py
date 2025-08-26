#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script for the Dental Voice Agent AI responses
This script demonstrates how the AI responds to common dental queries
"""

import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Dental practice data (same as in app.py)
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

AVAILABLE_SLOTS = [
    "Monday 9:00 AM", "Monday 10:00 AM", "Monday 2:00 PM", "Monday 3:00 PM",
    "Tuesday 9:00 AM", "Tuesday 10:00 AM", "Tuesday 2:00 PM", "Tuesday 3:00 PM",
    "Wednesday 9:00 AM", "Wednesday 10:00 AM", "Wednesday 2:00 PM", "Wednesday 3:00 PM",
    "Thursday 9:00 AM", "Thursday 10:00 AM", "Thursday 2:00 PM", "Thursday 3:00 PM",
    "Friday 9:00 AM", "Friday 10:00 AM", "Friday 2:00 PM"
]

def get_ai_response(user_query):
    """Get AI response for dental queries (same as in app.py)"""
    try:
        system_prompt = f"""You are a helpful dental office assistant for {DENTAL_DATA['practice_name']}. 
        You help patients with appointment scheduling, insurance questions, and general dental inquiries.
        
        Practice Information:
        - Name: {DENTAL_DATA['practice_name']}
        - Address: {DENTAL_DATA['address']}
        - Phone: {DENTAL_DATA['phone']}
        - Hours: {DENTAL_DATA['hours']}
        - Services: {', '.join(DENTAL_DATA['services'])}
        - Accepted Insurance: {', '.join(DENTAL_DATA['insurance'])}
        - Available appointment slots: {', '.join(AVAILABLE_SLOTS)}
        
        Be friendly, professional, and helpful. If someone asks about appointments, offer available slots.
        If they ask about insurance, explain what we accept. Keep responses concise and natural for voice interaction."""
        
        response = openai.ChatCompletion.create(
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
        return f"I'm sorry, I'm having trouble processing your request right now. Please try again or call us at {DENTAL_DATA['phone']}."

def demo_queries():
    """Demo common dental queries"""
    
    # Common dental queries to test
    demo_questions = [
        "What are your office hours?",
        "Do you accept Delta Dental insurance?",
        "I need to schedule an appointment for a cleaning",
        "What services do you offer?",
        "How much does a teeth cleaning cost?",
        "Do you have any appointments available this week?",
        "What should I do if I have a dental emergency?",
        "Do you offer teeth whitening services?",
        "What insurance providers do you accept?",
        "Can I schedule an appointment for next Monday?"
    ]
    
    print("🦷 Dental Voice Agent Demo")
    print("=" * 60)
    print(f"Practice: {DENTAL_DATA['practice_name']}")
    print(f"Phone: {DENTAL_DATA['phone']}")
    print("=" * 60)
    print()
    
    for i, question in enumerate(demo_questions, 1):
        print(f"🤔 Question {i}: {question}")
        print("-" * 40)
        
        try:
            response = get_ai_response(question)
            print(f"🤖 AI Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        print("=" * 60)
        print()

def interactive_demo():
    """Interactive demo where user can ask questions"""
    print("🦷 Interactive Dental Voice Agent Demo")
    print("=" * 50)
    print("Type your dental questions (or 'quit' to exit)")
    print("=" * 50)
    print()
    
    while True:
        try:
            question = input("🤔 Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for trying the demo!")
                break
            
            if not question:
                continue
            
            print("🤖 AI Response:", end=" ")
            response = get_ai_response(question)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print()

def main():
    """Main demo function"""
    print("🚀 Dental Voice Agent Demo")
    print("Choose an option:")
    print("1. Run predefined demo queries")
    print("2. Interactive demo (ask your own questions)")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                demo_queries()
                break
            elif choice == "2":
                interactive_demo()
                break
            elif choice == "3":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted. Goodbye!")
            break

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'your_openai_api_key_here':
        print("❌ Error: OpenAI API key not set!")
        print("Please:")
        print("1. Copy env.example to .env")
        print("2. Add your OpenAI API key to .env file")
        print("3. Run this demo again")
    else:
        main()
