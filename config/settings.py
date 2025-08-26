import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING = False
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///dental_practice.db')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '200'))
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
    
    # Email Configuration
    EMAIL_SERVER = os.getenv('EMAIL_SERVER', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@dentalpractice.com')
    
    # SMS Configuration
    SMS_API_KEY = os.getenv('SMS_API_KEY', '')
    SMS_API_URL = os.getenv('SMS_API_URL', '')
    
    # Dental Practice Configuration
    PRACTICE_NAME = os.getenv('PRACTICE_NAME', 'Bright Smile Dental Care')
    PRACTICE_PHONE = os.getenv('PRACTICE_PHONE', '(555) 123-4567')
    PRACTICE_ADDRESS = os.getenv('PRACTICE_ADDRESS', '123 Main Street, Anytown, CA 90210')
    PRACTICE_EMAIL = os.getenv('PRACTICE_EMAIL', 'info@brightsmiledental.com')
    
    # Office Hours
    OFFICE_HOURS = {
        'monday': {'start': '08:00', 'end': '18:00'},
        'tuesday': {'start': '08:00', 'end': '18:00'},
        'wednesday': {'start': '08:00', 'end': '18:00'},
        'thursday': {'start': '08:00', 'end': '18:00'},
        'friday': {'start': '08:00', 'end': '17:00'},
        'saturday': {'start': '09:00', 'end': '15:00'},
        'sunday': {'start': '00:00', 'end': '00:00'}  # Closed
    }
    
    # Services Configuration
    DENTAL_SERVICES = [
        {
            'name': 'General Checkup',
            'code': 'CHECKUP',
            'duration': 60,
            'base_price': 150.00,
            'description': 'Comprehensive dental examination and cleaning'
        },
        {
            'name': 'Teeth Cleaning',
            'code': 'CLEANING',
            'duration': 45,
            'base_price': 120.00,
            'description': 'Professional teeth cleaning and scaling'
        },
        {
            'name': 'Cavity Filling',
            'code': 'FILLING',
            'duration': 60,
            'base_price': 200.00,
            'description': 'Tooth cavity filling with composite material'
        },
        {
            'name': 'Root Canal',
            'code': 'ROOT_CANAL',
            'duration': 120,
            'base_price': 800.00,
            'description': 'Root canal treatment'
        },
        {
            'name': 'Teeth Whitening',
            'code': 'WHITENING',
            'duration': 90,
            'base_price': 300.00,
            'description': 'Professional teeth whitening treatment'
        },
        {
            'name': 'Dental Implants',
            'code': 'IMPLANT',
            'duration': 180,
            'base_price': 2500.00,
            'description': 'Dental implant placement'
        },
        {
            'name': 'Emergency Care',
            'code': 'EMERGENCY',
            'duration': 30,
            'base_price': 250.00,
            'description': 'Emergency dental care and consultation'
        }
    ]
    
    # Insurance Providers
    ACCEPTED_INSURANCE = [
        'Delta Dental',
        'Aetna',
        'Cigna',
        'Blue Cross Blue Shield',
        'MetLife',
        'UnitedHealthcare',
        'Humana',
        'Anthem',
        'Kaiser Permanente'
    ]
    
    # Notification Settings
    NOTIFICATION_SETTINGS = {
        'appointment_reminder_hours': 24,
        'payment_reminder_days': 7,
        'max_retry_attempts': 3,
        'retry_interval_minutes': 30
    }
    
    # Voice Assistant Settings
    VOICE_SETTINGS = {
        'speech_rate': 150,
        'speech_volume': 0.9,
        'recognition_timeout': 5,
        'phrase_time_limit': 10
    }
    
    # Security Settings
    SECURITY_SETTINGS = {
        'session_timeout_minutes': 30,
        'max_login_attempts': 5,
        'password_min_length': 8,
        'require_ssl': True
    }
    
    # File Upload Settings
    UPLOAD_SETTINGS = {
        'max_file_size': 10 * 1024 * 1024,  # 10MB
        'allowed_extensions': ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx'],
        'upload_folder': 'uploads'
    }
    
    # Analytics Settings
    ANALYTICS_SETTINGS = {
        'enable_tracking': True,
        'retention_days': 365,
        'export_format': 'json'
    }
    
    @classmethod
    def get_service_by_code(cls, service_code: str) -> Dict[str, Any]:
        """Get service configuration by code"""
        for service in cls.DENTAL_SERVICES:
            if service['code'] == service_code.upper():
                return service
        return None
    
    @classmethod
    def get_service_by_name(cls, service_name: str) -> Dict[str, Any]:
        """Get service configuration by name"""
        for service in cls.DENTAL_SERVICES:
            if service['name'].lower() == service_name.lower():
                return service
        return None
    
    @classmethod
    def is_office_open(cls, day: str, time: str = None) -> bool:
        """Check if office is open on given day and time"""
        day_lower = day.lower()
        if day_lower not in cls.OFFICE_HOURS:
            return False
            
        hours = cls.OFFICE_HOURS[day_lower]
        if hours['start'] == '00:00' and hours['end'] == '00:00':
            return False
            
        if time:
            return hours['start'] <= time <= hours['end']
            
        return True
    
    @classmethod
    def get_office_hours_display(cls) -> Dict[str, str]:
        """Get office hours in display format"""
        display_hours = {}
        for day, hours in cls.OFFICE_HOURS.items():
            if hours['start'] == '00:00' and hours['end'] == '00:00':
                display_hours[day.title()] = 'Closed'
            else:
                display_hours[day.title()] = f"{hours['start']} - {hours['end']}"
        return display_hours

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with production settings
    SECURITY_SETTINGS = {
        'session_timeout_minutes': 60,
        'max_login_attempts': 3,
        'password_min_length': 12,
        'require_ssl': True
    }

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    
    # Use test database
    DATABASE_URL = 'sqlite:///test_dental_practice.db'
    
    # Disable external services
    EMAIL_USERNAME = ''
    EMAIL_PASSWORD = ''
    SMS_API_KEY = ''

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """Get configuration class by name"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])

def validate_config() -> Dict[str, Any]:
    """Validate configuration and return any issues"""
    issues = []
    warnings = []
    
    current_config = get_config()
    
    # Check required environment variables
    if not current_config.OPENAI_API_KEY:
        issues.append("OPENAI_API_KEY is not set")
    
    if not current_config.SECRET_KEY or current_config.SECRET_KEY == 'your-secret-key-here':
        warnings.append("SECRET_KEY should be changed in production")
    
    if not current_config.EMAIL_USERNAME:
        warnings.append("EMAIL_USERNAME not set - email notifications will be disabled")
    
    if not current_config.SMS_API_KEY:
        warnings.append("SMS_API_KEY not set - SMS notifications will be disabled")
    
    return {
        'issues': issues,
        'warnings': warnings,
        'config_valid': len(issues) == 0
    }
