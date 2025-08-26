#!/usr/bin/env python3
"""
Unit tests for the voice processor utility
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.voice_processor import VoiceProcessor

class TestVoiceProcessor(unittest.TestCase):
    """Test cases for VoiceProcessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.voice_processor = VoiceProcessor()
        
    def test_initialization(self):
        """Test VoiceProcessor initialization"""
        self.assertIsNotNone(self.voice_processor)
        self.assertIsNotNone(self.voice_processor.recognizer)
        self.assertIsNotNone(self.voice_processor.microphone)
        self.assertIsNotNone(self.voice_processor.dental_keywords)
        self.assertIsNotNone(self.voice_processor.intent_patterns)
        
    def test_dental_keywords_structure(self):
        """Test dental keywords are properly structured"""
        expected_categories = ['appointment', 'insurance', 'services', 'hours', 'payment', 'emergency']
        
        for category in expected_categories:
            self.assertIn(category, self.voice_processor.dental_keywords)
            self.assertIsInstance(self.voice_processor.dental_keywords[category], list)
            self.assertGreater(len(self.voice_processor.dental_keywords[category]), 0)
            
    def test_intent_patterns_structure(self):
        """Test intent patterns are properly structured"""
        expected_intents = [
            'schedule_appointment', 'check_availability', 'insurance_inquiry',
            'service_inquiry', 'office_hours', 'emergency'
        ]
        
        for intent in expected_intents:
            self.assertIn(intent, self.voice_processor.intent_patterns)
            self.assertIsInstance(self.voice_processor.intent_patterns[intent], list)
            self.assertGreater(len(self.voice_processor.intent_patterns[intent]), 0)
            
    def test_extract_intent_schedule_appointment(self):
        """Test intent extraction for appointment scheduling"""
        test_queries = [
            "I want to schedule an appointment",
            "Can I book an appointment",
            "I need to make an appointment",
            "Schedule appointment for tomorrow"
        ]
        
        for query in test_queries:
            intent, entities = self.voice_processor.extract_intent(query)
            self.assertEqual(intent, "schedule_appointment")
            
    def test_extract_intent_insurance_inquiry(self):
        """Test intent extraction for insurance inquiries"""
        test_queries = [
            "Do you accept insurance",
            "What insurance providers do you work with",
            "My insurance is Delta Dental",
            "Insurance coverage for cleaning"
        ]
        
        for query in test_queries:
            intent, entities = self.voice_processor.extract_intent(query)
            self.assertEqual(intent, "insurance_inquiry")
            
    def test_extract_intent_service_inquiry(self):
        """Test intent extraction for service inquiries"""
        test_queries = [
            "How much does a cleaning cost",
            "What services do you offer",
            "Price for teeth whitening",
            "Cost of filling"
        ]
        
        for query in test_queries:
            intent, entities = self.voice_processor.extract_intent(query)
            self.assertEqual(intent, "service_inquiry")
            
    def test_extract_intent_office_hours(self):
        """Test intent extraction for office hours inquiries"""
        test_queries = [
            "What are your hours",
            "When are you open",
            "Office hours",
            "Are you open on weekends"
        ]
        
        for query in test_queries:
            intent, entities = self.voice_processor.extract_intent(query)
            self.assertEqual(intent, "office_hours")
            
    def test_extract_intent_emergency(self):
        """Test intent extraction for emergency inquiries"""
        test_queries = [
            "I have an emergency",
            "Severe tooth pain",
            "Broken tooth",
            "Urgent dental care"
        ]
        
        for query in test_queries:
            intent, entities = self.voice_processor.extract_intent(query)
            self.assertEqual(intent, "emergency")
            
    def test_extract_entities_appointment(self):
        """Test entity extraction for appointment scheduling"""
        query = "I want to schedule a cleaning appointment for tomorrow morning"
        intent, entities = self.voice_processor.extract_intent(query)
        
        self.assertEqual(intent, "schedule_appointment")
        self.assertIn("preferred_time", entities)
        self.assertIn("service_type", entities)
        self.assertEqual(entities["preferred_time"], "tomorrow")
        self.assertEqual(entities["service_type"], "cleaning")
        
    def test_extract_entities_insurance(self):
        """Test entity extraction for insurance inquiries"""
        query = "I have Delta Dental insurance"
        intent, entities = self.voice_processor.extract_intent(query)
        
        self.assertEqual(intent, "insurance_inquiry")
        self.assertIn("insurance_provider", entities)
        self.assertEqual(entities["insurance_provider"], "delta dental")
        
    def test_extract_entities_service(self):
        """Test entity extraction for service inquiries"""
        query = "How much does teeth whitening cost"
        intent, entities = self.voice_processor.extract_intent(query)
        
        self.assertEqual(intent, "service_inquiry")
        self.assertIn("service_type", entities)
        self.assertEqual(entities["service_type"], "whitening")
        
    def test_extract_entities_emergency(self):
        """Test entity extraction for emergency inquiries"""
        query = "I have severe tooth pain"
        intent, entities = self.voice_processor.extract_intent(query)
        
        self.assertEqual(intent, "emergency")
        self.assertIn("urgency_level", entities)
        self.assertEqual(entities["urgency_level"], "high")
        
    def test_generate_appointment_response(self):
        """Test appointment response generation"""
        entities = {
            "service_type": "cleaning",
            "preferred_time": "tomorrow"
        }
        
        response = self.voice_processor._generate_appointment_response(entities)
        
        self.assertIsInstance(response, str)
        self.assertIn("cleaning", response)
        self.assertIn("tomorrow", response)
        self.assertIn("appointment", response)
        
    def test_generate_insurance_response(self):
        """Test insurance response generation"""
        # Test with specific provider
        entities = {"insurance_provider": "delta dental"}
        response = self.voice_processor._generate_insurance_response(entities)
        
        self.assertIsInstance(response, str)
        self.assertIn("delta dental", response)
        
        # Test without provider
        entities = {}
        response = self.voice_processor._generate_insurance_response(entities)
        
        self.assertIsInstance(response, str)
        self.assertIn("insurance", response)
        
    def test_generate_service_response(self):
        """Test service response generation"""
        # Test with specific service
        entities = {"service_type": "cleaning"}
        response = self.voice_processor._generate_service_response(entities)
        
        self.assertIsInstance(response, str)
        self.assertIn("cleaning", response)
        self.assertIn("cost", response)
        
        # Test without service
        entities = {}
        response = self.voice_processor._generate_service_response(entities)
        
        self.assertIsInstance(response, str)
        self.assertIn("services", response)
        
    def test_generate_hours_response(self):
        """Test office hours response generation"""
        entities = {}
        response = self.voice_processor._generate_hours_response(entities)
        
        self.assertIsInstance(response, str)
        self.assertIn("hours", response)
        self.assertIn("Monday", response)
        self.assertIn("Friday", response)
        
    def test_generate_emergency_response(self):
        """Test emergency response generation"""
        # Test high urgency
        entities = {"urgency_level": "high"}
        response = self.voice_processor._generate_emergency_response(entities)
        
        self.assertIsInstance(response, str)
        self.assertIn("emergency", response)
        self.assertIn("immediately", response)
        
        # Test medium urgency
        entities = {"urgency_level": "medium"}
        response = self.voice_processor._generate_emergency_response(entities)
        
        self.assertIsInstance(response, str)
        self.assertIn("emergency", response)
        
    def test_generate_general_response(self):
        """Test general response generation"""
        # Test with appointment keywords
        entities = {"query": "I want to schedule an appointment"}
        response = self.voice_processor._generate_general_response(entities)
        
        self.assertIsInstance(response, str)
        self.assertIn("appointment", response)
        
        # Test with insurance keywords
        entities = {"query": "Do you accept insurance"}
        response = self.voice_processor._generate_general_response(entities)
        
        self.assertIsInstance(response, str)
        self.assertIn("insurance", response)
        
    def test_process_voice_query_with_text(self):
        """Test voice query processing with text input"""
        query = "I want to schedule a cleaning appointment"
        result = self.voice_processor.process_voice_query(query)
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result["success"])
        self.assertEqual(result["original_text"], query)
        self.assertEqual(result["intent"], "schedule_appointment")
        self.assertIn("response", result)
        
    def test_process_voice_query_no_text(self):
        """Test voice query processing without text input"""
        # Mock the listen_for_speech method to return None
        with patch.object(self.voice_processor, 'listen_for_speech', return_value=None):
            result = self.voice_processor.process_voice_query()
            
            self.assertIsInstance(result, dict)
            self.assertFalse(result["success"])
            self.assertIn("error", result)
            self.assertIn("response", result)
            
    @patch('utils.voice_processor.sr.Recognizer')
    @patch('utils.voice_processor.sr.Microphone')
    def test_listen_for_speech_success(self, mock_microphone, mock_recognizer):
        """Test successful speech recognition"""
        # Mock the recognizer to return a successful result
        mock_recognizer_instance = Mock()
        mock_recognizer_instance.recognize_google.return_value = "Hello world"
        mock_recognizer.return_value = mock_recognizer_instance
        
        # Mock the microphone context manager
        mock_mic = Mock()
        mock_microphone.return_value = mock_mic
        
        # Create a new instance to use the mocked components
        processor = VoiceProcessor()
        processor.recognizer = mock_recognizer_instance
        processor.microphone = mock_mic
        
        result = processor.listen_for_speech()
        
        self.assertEqual(result, "hello world")
        
    @patch('utils.voice_processor.sr.Recognizer')
    @patch('utils.voice_processor.sr.Microphone')
    def test_listen_for_speech_timeout(self, mock_microphone, mock_recognizer):
        """Test speech recognition timeout"""
        # Mock the recognizer to raise a timeout error
        mock_recognizer_instance = Mock()
        mock_recognizer_instance.listen.side_effect = sr.WaitTimeoutError()
        mock_recognizer.return_value = mock_recognizer_instance
        
        # Mock the microphone context manager
        mock_mic = Mock()
        mock_microphone.return_value = mock_mic
        
        # Create a new instance to use the mocked components
        processor = VoiceProcessor()
        processor.recognizer = mock_recognizer_instance
        processor.microphone = mock_mic
        
        result = processor.listen_for_speech()
        
        self.assertIsNone(result)
        
    @patch('utils.voice_processor.sr.Recognizer')
    @patch('utils.voice_processor.sr.Microphone')
    def test_listen_for_speech_unknown_value(self, mock_microphone, mock_recognizer):
        """Test speech recognition with unknown value"""
        # Mock the recognizer to raise an unknown value error
        mock_recognizer_instance = Mock()
        mock_recognizer_instance.listen.side_effect = sr.UnknownValueError()
        mock_recognizer.return_value = mock_recognizer_instance
        
        # Mock the microphone context manager
        mock_mic = Mock()
        mock_microphone.return_value = mock_mic
        
        # Create a new instance to use the mocked components
        processor = VoiceProcessor()
        processor.recognizer = mock_recognizer_instance
        processor.microphone = mock_mic
        
        result = processor.listen_for_speech()
        
        self.assertIsNone(result)
        
    @patch('utils.voice_processor.pyttsx3.init')
    def test_speak_text_success(self, mock_init):
        """Test successful text-to-speech"""
        # Mock the text-to-speech engine
        mock_engine = Mock()
        mock_init.return_value = mock_engine
        
        # Create a new instance to use the mocked engine
        processor = VoiceProcessor()
        processor.engine = mock_engine
        
        processor.speak_text("Hello world")
        
        # Verify the engine methods were called
        mock_engine.setProperty.assert_called()
        mock_engine.say.assert_called_with("Hello world")
        mock_engine.runAndWait.assert_called()
        
    @patch('utils.voice_processor.pyttsx3.init')
    def test_speak_text_no_engine(self, mock_init):
        """Test text-to-speech without engine"""
        # Mock the init to raise an exception
        mock_init.side_effect = Exception("Engine not available")
        
        # Create a new instance
        processor = VoiceProcessor()
        
        # Should not raise an exception
        processor.speak_text("Hello world")
        
    def test_continuous_listening_start_stop(self):
        """Test continuous listening start and stop"""
        # Mock the process_voice_query method
        with patch.object(self.voice_processor, 'process_voice_query') as mock_process:
            mock_process.return_value = {"success": True}
            
            # Start continuous listening
            callback_called = False
            def test_callback(result):
                nonlocal callback_called
                callback_called = True
                
            self.voice_processor.start_continuous_listening(test_callback)
            
            # Stop continuous listening
            self.voice_processor.stop_continuous_listening()
            
            # Verify the callback was called
            self.assertTrue(callback_called)
            
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Test empty string
        intent, entities = self.voice_processor.extract_intent("")
        self.assertEqual(intent, "general_inquiry")
        
        # Test very long string
        long_query = "a" * 1000
        intent, entities = self.voice_processor.extract_intent(long_query)
        self.assertEqual(intent, "general_inquiry")
        
        # Test special characters
        special_query = "!@#$%^&*()"
        intent, entities = self.voice_processor.extract_intent(special_query)
        self.assertEqual(intent, "general_inquiry")
        
        # Test numbers only
        number_query = "12345"
        intent, entities = self.voice_processor.extract_intent(number_query)
        self.assertEqual(intent, "general_inquiry")

if __name__ == '__main__':
    unittest.main()
