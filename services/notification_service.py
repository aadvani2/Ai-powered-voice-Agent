from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

class NotificationType:
    APPOINTMENT_REMINDER = "appointment_reminder"
    APPOINTMENT_CONFIRMATION = "appointment_confirmation"
    APPOINTMENT_CANCELLATION = "appointment_cancellation"
    APPOINTMENT_RESCHEDULE = "appointment_reschedule"
    PAYMENT_REMINDER = "payment_reminder"
    INSURANCE_UPDATE = "insurance_update"
    GENERAL_MESSAGE = "general_message"

class NotificationChannel:
    EMAIL = "email"
    SMS = "sms"
    VOICE = "voice"
    PUSH = "push"

class Notification:
    def __init__(self, notification_id: str, recipient_id: str, notification_type: str,
                 channel: str, subject: str, message: str, scheduled_time: datetime):
        self.notification_id = notification_id
        self.recipient_id = recipient_id
        self.notification_type = notification_type
        self.channel = channel
        self.subject = subject
        self.message = message
        self.scheduled_time = scheduled_time
        self.sent_time = None
        self.status = "pending"  # pending, sent, failed, cancelled
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.retry_count = 0
        self.max_retries = 3
        self.error_message = ""
        
    def to_dict(self) -> Dict:
        return {
            'notification_id': self.notification_id,
            'recipient_id': self.recipient_id,
            'notification_type': self.notification_type,
            'channel': self.channel,
            'subject': self.subject,
            'message': self.message,
            'scheduled_time': self.scheduled_time.isoformat(),
            'sent_time': self.sent_time.isoformat() if self.sent_time else None,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'retry_count': self.retry_count,
            'error_message': self.error_message
        }

class NotificationService:
    def __init__(self, data_file: str = "data/notifications.json"):
        self.data_file = data_file
        self.notifications = {}
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': os.getenv('EMAIL_USERNAME', ''),
            'password': os.getenv('EMAIL_PASSWORD', ''),
            'from_email': os.getenv('FROM_EMAIL', 'noreply@dentalpractice.com')
        }
        self.sms_config = {
            'api_key': os.getenv('SMS_API_KEY', ''),
            'api_url': os.getenv('SMS_API_URL', '')
        }
        self._load_notifications()
        
    def _load_notifications(self):
        """Load notifications from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for notification_data in data.values():
                        notification = self._create_notification_from_dict(notification_data)
                        self.notifications[notification.notification_id] = notification
            except Exception as e:
                print(f"Error loading notifications: {e}")
                
    def _save_notifications(self):
        """Save notifications to JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        try:
            with open(self.data_file, 'w') as f:
                json.dump({nid: notification.to_dict() for nid, notification in self.notifications.items()}, f, indent=2)
        except Exception as e:
            print(f"Error saving notifications: {e}")
            
    def _create_notification_from_dict(self, data: Dict) -> Notification:
        """Create a Notification object from dictionary data"""
        notification = Notification(
            notification_id=data['notification_id'],
            recipient_id=data['recipient_id'],
            notification_type=data['notification_type'],
            channel=data['channel'],
            subject=data['subject'],
            message=data['message'],
            scheduled_time=datetime.fromisoformat(data['scheduled_time'])
        )
        
        # Restore additional data
        notification.sent_time = datetime.fromisoformat(data['sent_time']) if data.get('sent_time') else None
        notification.status = data['status']
        notification.retry_count = data.get('retry_count', 0)
        notification.error_message = data.get('error_message', '')
        notification.created_at = datetime.fromisoformat(data['created_at'])
        notification.updated_at = datetime.fromisoformat(data['updated_at'])
        
        return notification
        
    def create_notification(self, recipient_id: str, notification_type: str, channel: str,
                          subject: str, message: str, scheduled_time: datetime) -> Notification:
        """Create a new notification"""
        notification_id = f"NOT{len(self.notifications) + 1:04d}"
        notification = Notification(
            notification_id=notification_id,
            recipient_id=recipient_id,
            notification_type=notification_type,
            channel=channel,
            subject=subject,
            message=message,
            scheduled_time=scheduled_time
        )
        
        self.notifications[notification_id] = notification
        self._save_notifications()
        return notification
        
    def send_appointment_reminder(self, patient_id: str, appointment_id: str, 
                                appointment_date: datetime, patient_email: str, 
                                patient_phone: str = "") -> List[Notification]:
        """Send appointment reminder notifications"""
        notifications = []
        
        # Email reminder
        subject = "Appointment Reminder"
        message = f"""
        Dear Patient,
        
        This is a friendly reminder about your upcoming dental appointment:
        
        Date: {appointment_date.strftime('%B %d, %Y at %I:%M %p')}
        Appointment ID: {appointment_id}
        
        Please arrive 10 minutes before your scheduled time.
        
        If you need to reschedule or cancel, please call us at (555) 123-4567.
        
        Best regards,
        Bright Smile Dental Care
        """
        
        # Schedule email reminder 24 hours before
        email_time = appointment_date - timedelta(hours=24)
        if email_time > datetime.now():
            email_notification = self.create_notification(
                patient_id, NotificationType.APPOINTMENT_REMINDER, 
                NotificationChannel.EMAIL, subject, message, email_time
            )
            notifications.append(email_notification)
        
        # SMS reminder if phone provided
        if patient_phone:
            sms_message = f"Reminder: Your dental appointment is tomorrow at {appointment_date.strftime('%I:%M %p')}. Call (555) 123-4567 to reschedule."
            sms_time = appointment_date - timedelta(hours=12)
            if sms_time > datetime.now():
                sms_notification = self.create_notification(
                    patient_id, NotificationType.APPOINTMENT_REMINDER,
                    NotificationChannel.SMS, "Appointment Reminder", sms_message, sms_time
                )
                notifications.append(sms_notification)
                
        return notifications
        
    def send_appointment_confirmation(self, patient_id: str, appointment_id: str,
                                    appointment_date: datetime, patient_email: str) -> Notification:
        """Send appointment confirmation"""
        subject = "Appointment Confirmation"
        message = f"""
        Dear Patient,
        
        Your dental appointment has been confirmed:
        
        Date: {appointment_date.strftime('%B %d, %Y at %I:%M %p')}
        Appointment ID: {appointment_id}
        
        Please arrive 10 minutes before your scheduled time.
        
        If you need to reschedule or cancel, please call us at (555) 123-4567.
        
        Best regards,
        Bright Smile Dental Care
        """
        
        notification = self.create_notification(
            patient_id, NotificationType.APPOINTMENT_CONFIRMATION,
            NotificationChannel.EMAIL, subject, message, datetime.now()
        )
        
        return notification
        
    def send_payment_reminder(self, patient_id: str, invoice_id: str, amount: float,
                            due_date: datetime, patient_email: str) -> Notification:
        """Send payment reminder"""
        subject = "Payment Reminder"
        message = f"""
        Dear Patient,
        
        This is a friendly reminder about your outstanding balance:
        
        Invoice ID: {invoice_id}
        Amount Due: ${amount:.2f}
        Due Date: {due_date.strftime('%B %d, %Y')}
        
        Please contact us to arrange payment or if you have any questions.
        
        Best regards,
        Bright Smile Dental Care
        """
        
        notification = self.create_notification(
            patient_id, NotificationType.PAYMENT_REMINDER,
            NotificationChannel.EMAIL, subject, message, datetime.now()
        )
        
        return notification
        
    def send_email(self, to_email: str, subject: str, message: str) -> bool:
        """Send email notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from_email']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            text = msg.as_string()
            server.sendmail(self.email_config['from_email'], to_email, text)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
            
    def send_sms(self, to_phone: str, message: str) -> bool:
        """Send SMS notification"""
        try:
            if not self.sms_config['api_key']:
                print("SMS API key not configured")
                return False
                
            payload = {
                'api_key': self.sms_config['api_key'],
                'to': to_phone,
                'message': message
            }
            
            response = requests.post(self.sms_config['api_url'], json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False
            
    def process_pending_notifications(self):
        """Process all pending notifications that are due"""
        now = datetime.now()
        pending_notifications = [
            n for n in self.notifications.values()
            if n.status == "pending" and n.scheduled_time <= now
        ]
        
        for notification in pending_notifications:
            self._send_notification(notification)
            
    def _send_notification(self, notification: Notification):
        """Send a single notification"""
        success = False
        
        try:
            if notification.channel == NotificationChannel.EMAIL:
                success = self.send_email(notification.recipient_id, notification.subject, notification.message)
            elif notification.channel == NotificationChannel.SMS:
                success = self.send_sms(notification.recipient_id, notification.message)
            # Add other channels as needed
            
            if success:
                notification.status = "sent"
                notification.sent_time = datetime.now()
            else:
                notification.retry_count += 1
                if notification.retry_count >= notification.max_retries:
                    notification.status = "failed"
                    notification.error_message = "Max retries exceeded"
                else:
                    notification.status = "pending"
                    # Reschedule for retry
                    notification.scheduled_time = datetime.now() + timedelta(minutes=30)
                    
        except Exception as e:
            notification.status = "failed"
            notification.error_message = str(e)
            
        notification.updated_at = datetime.now()
        self._save_notifications()
        
    def get_notification_statistics(self) -> Dict:
        """Get notification statistics"""
        total_notifications = len(self.notifications)
        status_counts = {}
        type_counts = {}
        channel_counts = {}
        
        for notification in self.notifications.values():
            # Status counts
            status = notification.status
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # Type counts
            ntype = notification.notification_type
            type_counts[ntype] = type_counts.get(ntype, 0) + 1
            
            # Channel counts
            channel = notification.channel
            channel_counts[channel] = channel_counts.get(channel, 0) + 1
            
        return {
            "total_notifications": total_notifications,
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "channel_distribution": channel_counts,
            "pending_notifications": len([n for n in self.notifications.values() if n.status == "pending"]),
            "failed_notifications": len([n for n in self.notifications.values() if n.status == "failed"])
        }
