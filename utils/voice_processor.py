import speech_recognition as sr
import pyttsx3
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import threading
import queue

class VoiceProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = None
        self.audio_queue = queue.Queue()
        self.is_listening = False
        
        # Initialize text-to-speech engine
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
        except Exception as e:
            print(f"Warning: Could not initialize text-to-speech engine: {e}")
            
        # Dental-specific keywords and patterns
        self.dental_keywords = {
            'appointment': ['appointment', 'schedule', 'book', 'reschedule', 'cancel'],
            'insurance': ['insurance', 'coverage', 'provider', 'policy'],
            'services': ['cleaning', 'filling', 'whitening', 'checkup', 'emergency'],
            'hours': ['hours', 'open', 'closed', 'available', 'time'],
            'payment': ['payment', 'bill', 'cost', 'price', 'invoice'],
            'emergency': ['emergency', 'urgent', 'pain', 'hurt', 'broken']
        }
        
        # Intent patterns
        self.intent_patterns = {
            'schedule_appointment': [
                r'(schedule|book|make)\s+(an?\s+)?appointment',
                r'(want|need)\s+(to\s+)?(schedule|book)\s+(an?\s+)?appointment',
                r'appointment\s+(for|on)\s+(\w+)',
                r'(when|what)\s+(time|day)\s+(are|do)\s+(you|they)\s+(have|available)'
            ],
            'check_availability': [
                r'(available|open|free)\s+(time|slot|appointment)',
                r'(what|when)\s+(are|do)\s+(you|they)\s+(have|available)',
                r'(next|upcoming)\s+(available|open)\s+(time|slot)'
            ],
            'insurance_inquiry': [
                r'(accept|take|work\s+with)\s+(insurance|coverage)',
                r'(what|which)\s+(insurance|provider)\s+(do\s+you|are\s+accepted)',
                r'(my|the)\s+(insurance|provider)\s+(is|are)',
                r'(coverage|benefits)\s+(for|of)'
            ],
            'service_inquiry': [
                r'(what|which)\s+(services|treatments)\s+(do\s+you|are\s+offered)',
                r'(cost|price|how\s+much)\s+(for|is)\s+(\w+)',
                r'(cleaning|filling|whitening|checkup)\s+(cost|price)'
            ],
            'office_hours': [
                r'(what|when)\s+(are|do)\s+(you|they)\s+(open|close)',
                r'(hours|schedule)\s+(of\s+operation)?',
                r'(open|closed)\s+(on|during)'
            ],
            'emergency': [
                r'(emergency|urgent|pain|hurt)',
                r'(broken|cracked|chipped)\s+(tooth|teeth)',
                r'(severe|bad|terrible)\s+(pain|ache)'
            ]
        }
        
    def listen_for_speech(self, timeout: int = 5) -> Optional[str]:
        """Listen for speech input and return transcribed text"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
            return None
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None
            
    def speak_text(self, text: str, rate: int = 150, volume: float = 0.9):
        """Convert text to speech"""
        if not self.engine:
            print(f"Text-to-speech not available: {text}")
            return
            
        try:
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
            
    def extract_intent(self, text: str) -> Tuple[str, Dict]:
        """Extract intent and entities from text"""
        text = text.lower().strip()
        
        # Check for intent patterns
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    entities = self.extract_entities(text, intent)
                    return intent, entities
                    
        # Default to general inquiry
        return "general_inquiry", {"query": text}
        
    def extract_entities(self, text: str, intent: str) -> Dict:
        """Extract relevant entities from text based on intent"""
        entities = {"original_text": text}
        
        if intent == "schedule_appointment":
            # Extract date/time information
            date_patterns = [
                r'(today|tomorrow|next\s+\w+)',
                r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})',
                r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
                r'(morning|afternoon|evening|night)'
            ]
            
            for pattern in date_patterns:
                match = re.search(pattern, text)
                if match:
                    entities["preferred_time"] = match.group(0)
                    break
                    
            # Extract service type
            service_keywords = self.dental_keywords['services']
            for service in service_keywords:
                if service in text:
                    entities["service_type"] = service
                    break
                    
        elif intent == "insurance_inquiry":
            # Extract insurance provider names
            insurance_providers = [
                'delta dental', 'aetna', 'cigna', 'blue cross', 'metlife', 'unitedhealthcare'
            ]
            
            for provider in insurance_providers:
                if provider in text:
                    entities["insurance_provider"] = provider
                    break
                    
        elif intent == "service_inquiry":
            # Extract service type
            service_keywords = self.dental_keywords['services']
            for service in service_keywords:
                if service in text:
                    entities["service_type"] = service
                    break
                    
        elif intent == "emergency":
            # Extract urgency level
            urgency_words = ['severe', 'bad', 'terrible', 'excruciating', 'unbearable']
            for word in urgency_words:
                if word in text:
                    entities["urgency_level"] = "high"
                    break
            else:
                entities["urgency_level"] = "medium"
                
        return entities
        
    def generate_response(self, intent: str, entities: Dict) -> str:
        """Generate appropriate response based on intent and entities"""
        if intent == "schedule_appointment":
            return self._generate_appointment_response(entities)
        elif intent == "check_availability":
            return self._generate_availability_response(entities)
        elif intent == "insurance_inquiry":
            return self._generate_insurance_response(entities)
        elif intent == "service_inquiry":
            return self._generate_service_response(entities)
        elif intent == "office_hours":
            return self._generate_hours_response(entities)
        elif intent == "emergency":
            return self._generate_emergency_response(entities)
        else:
            return self._generate_general_response(entities)
            
    def _generate_appointment_response(self, entities: Dict) -> str:
        """Generate response for appointment scheduling"""
        service_type = entities.get("service_type", "appointment")
        preferred_time = entities.get("preferred_time", "")
        
        response = f"I'd be happy to help you schedule a {service_type} appointment."
        
        if preferred_time:
            response += f" You mentioned {preferred_time}. "
            
        response += "Let me check our available slots. What's your preferred date and time?"
        
        return response
        
    def _generate_availability_response(self, entities: Dict) -> str:
        """Generate response for availability check"""
        return "I can check our available appointment slots for you. What date are you looking for?"
        
    def _generate_insurance_response(self, entities: Dict) -> str:
        """Generate response for insurance inquiries"""
        provider = entities.get("insurance_provider", "")
        
        if provider:
            return f"Yes, we do accept {provider} insurance. Would you like me to check your specific coverage?"
        else:
            return "We accept most major insurance providers including Delta Dental, Aetna, Cigna, Blue Cross Blue Shield, MetLife, and UnitedHealthcare. Which provider do you have?"
            
    def _generate_service_response(self, entities: Dict) -> str:
        """Generate response for service inquiries"""
        service_type = entities.get("service_type", "")
        
        if service_type:
            return f"For {service_type}, our prices typically range from $100 to $500 depending on the specific treatment needed. Would you like me to schedule a consultation to get a more accurate estimate?"
        else:
            return "We offer a wide range of dental services including cleanings, fillings, root canals, teeth whitening, and emergency care. Which service are you interested in?"
            
    def _generate_hours_response(self, entities: Dict) -> str:
        """Generate response for office hours inquiries"""
        return "Our office hours are Monday through Friday 8 AM to 6 PM, Saturday 9 AM to 3 PM, and we're closed on Sundays. We also offer emergency appointments outside of regular hours."
        
    def _generate_emergency_response(self, entities: Dict) -> str:
        """Generate response for emergency inquiries"""
        urgency = entities.get("urgency_level", "medium")
        
        if urgency == "high":
            return "I understand this is an emergency. Please call our emergency line at (555) 123-4567 immediately, or if it's after hours, call (555) 999-8888 for urgent dental care."
        else:
            return "I can help you schedule an emergency appointment. How soon do you need to be seen?"
            
    def _generate_general_response(self, entities: Dict) -> str:
        """Generate response for general inquiries"""
        query = entities.get("query", "")
        
        if any(keyword in query for keyword in self.dental_keywords['appointment']):
            return "I can help you with appointment scheduling. Would you like to book an appointment?"
        elif any(keyword in query for keyword in self.dental_keywords['insurance']):
            return "I can help you with insurance questions. What would you like to know about your coverage?"
        else:
            return "I'm here to help with your dental care needs. How can I assist you today?"
            
    def process_voice_query(self, text: str = None) -> Dict:
        """Process a voice query and return structured response"""
        if not text:
            text = self.listen_for_speech()
            
        if not text:
            return {
                "success": False,
                "error": "No speech detected",
                "response": "I didn't catch that. Could you please repeat?"
            }
            
        # Extract intent and entities
        intent, entities = self.extract_intent(text)
        
        # Generate response
        response = self.generate_response(intent, entities)
        
        return {
            "success": True,
            "original_text": text,
            "intent": intent,
            "entities": entities,
            "response": response
        }
        
    def start_continuous_listening(self, callback):
        """Start continuous listening for voice input"""
        self.is_listening = True
        
        def listen_loop():
            while self.is_listening:
                result = self.process_voice_query()
                if result["success"]:
                    callback(result)
                    
        thread = threading.Thread(target=listen_loop)
        thread.daemon = True
        thread.start()
        
    def stop_continuous_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
