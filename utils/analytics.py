from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import os
from collections import defaultdict, Counter

class AnalyticsEngine:
    def __init__(self, data_directory: str = "data"):
        self.data_directory = data_directory
        
    def load_data(self, filename: str) -> Dict:
        """Load data from JSON file"""
        filepath = os.path.join(self.data_directory, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        return {}
        
    def generate_practice_overview(self) -> Dict:
        """Generate comprehensive practice overview"""
        patients_data = self.load_data("patients.json")
        appointments_data = self.load_data("appointments.json")
        billing_data = self.load_data("billing.json")
        
        total_patients = len(patients_data)
        total_appointments = len(appointments_data)
        
        # Calculate revenue metrics
        invoices = billing_data.get('invoices', {})
        total_revenue = sum(inv.get('total_amount', 0) for inv in invoices.values())
        total_paid = sum(inv.get('paid_amount', 0) for inv in invoices.values())
        outstanding_balance = sum(inv.get('balance_due', 0) for inv in invoices.values())
        
        # Appointment statistics
        appointment_statuses = Counter()
        appointment_types = Counter()
        
        for appt in appointments_data.values():
            appointment_statuses[appt.get('status', 'unknown')] += 1
            appointment_types[appt.get('appointment_type', 'unknown')] += 1
            
        return {
            "practice_overview": {
                "total_patients": total_patients,
                "total_appointments": total_appointments,
                "total_revenue": total_revenue,
                "total_paid": total_paid,
                "outstanding_balance": outstanding_balance,
                "collection_rate": (total_paid / total_revenue * 100) if total_revenue > 0 else 0
            },
            "appointment_analytics": {
                "status_distribution": dict(appointment_statuses),
                "type_distribution": dict(appointment_types)
            }
        }
        
    def generate_patient_analytics(self) -> Dict:
        """Generate patient-related analytics"""
        patients_data = self.load_data("patients.json")
        
        if not patients_data:
            return {}
            
        # Age distribution
        age_groups = {"0-17": 0, "18-30": 0, "31-50": 0, "51-70": 0, "70+": 0}
        insurance_providers = Counter()
        new_patients_monthly = defaultdict(int)
        
        for patient in patients_data.values():
            # Age calculation (simplified)
            dob = patient.get('date_of_birth', '')
            if dob:
                try:
                    birth_year = int(dob.split('-')[0])
                    age = datetime.now().year - birth_year
                    if age < 18:
                        age_groups["0-17"] += 1
                    elif age < 31:
                        age_groups["18-30"] += 1
                    elif age < 51:
                        age_groups["31-50"] += 1
                    elif age < 71:
                        age_groups["51-70"] += 1
                    else:
                        age_groups["70+"] += 1
                except:
                    pass
                    
            # Insurance provider
            provider = patient.get('insurance_provider')
            if provider:
                insurance_providers[provider] += 1
                
            # New patients by month
            created_at = patient.get('created_at', '')
            if created_at:
                try:
                    month = created_at[:7]  # YYYY-MM
                    new_patients_monthly[month] += 1
                except:
                    pass
                    
        return {
            "patient_demographics": {
                "age_distribution": age_groups,
                "insurance_coverage": {
                    "with_insurance": sum(insurance_providers.values()),
                    "without_insurance": total_patients - sum(insurance_providers.values()),
                    "insurance_providers": dict(insurance_providers)
                }
            },
            "patient_growth": {
                "new_patients_by_month": dict(new_patients_monthly),
                "total_patients": len(patients_data)
            }
        }
        
    def generate_revenue_analytics(self) -> Dict:
        """Generate revenue and financial analytics"""
        billing_data = self.load_data("billing.json")
        invoices = billing_data.get('invoices', {})
        
        if not invoices:
            return {}
            
        # Revenue by month
        revenue_by_month = defaultdict(float)
        payments_by_month = defaultdict(float)
        
        for invoice in invoices.values():
            created_date = invoice.get('created_date', '')
            if created_date:
                month = created_date[:7]  # YYYY-MM
                revenue_by_month[month] += invoice.get('total_amount', 0)
                payments_by_month[month] += invoice.get('paid_amount', 0)
                
        # Payment method analysis
        payment_methods = Counter()
        invoice_statuses = Counter()
        
        for invoice in invoices.values():
            status = invoice.get('status', 'unknown')
            invoice_statuses[status] += 1
            
        return {
            "revenue_analysis": {
                "revenue_by_month": dict(revenue_by_month),
                "payments_by_month": dict(payments_by_month),
                "total_revenue": sum(inv.get('total_amount', 0) for inv in invoices.values()),
                "total_paid": sum(inv.get('paid_amount', 0) for inv in invoices.values()),
                "outstanding_balance": sum(inv.get('balance_due', 0) for inv in invoices.values())
            },
            "invoice_analysis": {
                "status_distribution": dict(invoice_statuses),
                "average_invoice_amount": sum(inv.get('total_amount', 0) for inv in invoices.values()) / len(invoices) if invoices else 0
            }
        }
        
    def generate_appointment_analytics(self) -> Dict:
        """Generate appointment-related analytics"""
        appointments_data = self.load_data("appointments.json")
        
        if not appointments_data:
            return {}
            
        # Appointment trends by month
        appointments_by_month = defaultdict(int)
        appointments_by_day_of_week = defaultdict(int)
        appointments_by_hour = defaultdict(int)
        
        for appointment in appointments_data.values():
            scheduled_date = appointment.get('scheduled_date', '')
            if scheduled_date:
                try:
                    dt = datetime.fromisoformat(scheduled_date)
                    month = dt.strftime('%Y-%m')
                    day_of_week = dt.strftime('%A')
                    hour = dt.hour
                    
                    appointments_by_month[month] += 1
                    appointments_by_day_of_week[day_of_week] += 1
                    appointments_by_hour[hour] += 1
                except:
                    pass
                    
        return {
            "appointment_trends": {
                "by_month": dict(appointments_by_month),
                "by_day_of_week": dict(appointments_by_day_of_week),
                "by_hour": dict(appointments_by_hour)
            },
            "appointment_metrics": {
                "total_appointments": len(appointments_data),
                "average_appointments_per_month": len(appointments_data) / max(len(appointments_by_month), 1)
            }
        }
        
    def generate_operational_analytics(self) -> Dict:
        """Generate operational efficiency analytics"""
        appointments_data = self.load_data("appointments.json")
        patients_data = self.load_data("patients.json")
        
        # Calculate operational metrics
        total_appointments = len(appointments_data)
        completed_appointments = len([a for a in appointments_data.values() if a.get('status') == 'completed'])
        cancelled_appointments = len([a for a in appointments_data.values() if a.get('status') == 'cancelled'])
        
        # Patient retention (simplified)
        patient_appointment_counts = Counter()
        for appointment in appointments_data.values():
            patient_id = appointment.get('patient_id')
            if patient_id:
                patient_appointment_counts[patient_id] += 1
                
        returning_patients = len([pid for pid, count in patient_appointment_counts.items() if count > 1])
        new_patients = len([pid for pid, count in patient_appointment_counts.items() if count == 1])
        
        return {
            "operational_metrics": {
                "completion_rate": (completed_appointments / total_appointments * 100) if total_appointments > 0 else 0,
                "cancellation_rate": (cancelled_appointments / total_appointments * 100) if total_appointments > 0 else 0,
                "patient_retention": {
                    "returning_patients": returning_patients,
                    "new_patients": new_patients,
                    "retention_rate": (returning_patients / len(patient_appointment_counts) * 100) if patient_appointment_counts else 0
                }
            }
        }
        
    def generate_comprehensive_report(self) -> Dict:
        """Generate a comprehensive analytics report"""
        return {
            "report_generated": datetime.now().isoformat(),
            "practice_overview": self.generate_practice_overview(),
            "patient_analytics": self.generate_patient_analytics(),
            "revenue_analytics": self.generate_revenue_analytics(),
            "appointment_analytics": self.generate_appointment_analytics(),
            "operational_analytics": self.generate_operational_analytics()
        }
        
    def export_report_to_json(self, filename: str = None) -> str:
        """Export analytics report to JSON file"""
        if not filename:
            filename = f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        report = self.generate_comprehensive_report()
        
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            return filepath
        except Exception as e:
            print(f"Error exporting report: {e}")
            return None
            
    def get_key_performance_indicators(self) -> Dict:
        """Get key performance indicators"""
        practice_overview = self.generate_practice_overview()
        patient_analytics = self.generate_patient_analytics()
        revenue_analytics = self.generate_revenue_analytics()
        operational_analytics = self.generate_operational_analytics()
        
        return {
            "kpis": {
                "total_patients": practice_overview.get("practice_overview", {}).get("total_patients", 0),
                "total_revenue": practice_overview.get("practice_overview", {}).get("total_revenue", 0),
                "collection_rate": practice_overview.get("practice_overview", {}).get("collection_rate", 0),
                "completion_rate": operational_analytics.get("operational_metrics", {}).get("completion_rate", 0),
                "patient_retention_rate": operational_analytics.get("operational_metrics", {}).get("patient_retention", {}).get("retention_rate", 0),
                "average_invoice_amount": revenue_analytics.get("invoice_analysis", {}).get("average_invoice_amount", 0)
            }
        }
