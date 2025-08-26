#!/usr/bin/env python3
"""
Analytics report generator for the dental voice agent
This script generates comprehensive reports and exports them
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.analytics import AnalyticsEngine
from services.patient_service import PatientService
from services.appointment_service import AppointmentService
from services.billing_service import BillingService

def generate_practice_report():
    """Generate a comprehensive practice report"""
    print("📊 Generating Practice Analytics Report...")
    print("=" * 50)
    
    analytics = AnalyticsEngine()
    
    # Generate comprehensive report
    report = analytics.generate_comprehensive_report()
    
    # Export to JSON
    filename = analytics.export_report_to_json()
    
    if filename:
        print(f"✅ Report exported to: {filename}")
    else:
        print("❌ Failed to export report")
        
    return report

def generate_patient_report():
    """Generate detailed patient analytics"""
    print("\n👥 Generating Patient Analytics...")
    
    patient_service = PatientService()
    stats = patient_service.get_patient_statistics()
    
    print(f"📈 Total Patients: {stats['total_patients']}")
    print(f"🏥 Patients with Insurance: {stats['patients_with_insurance']}")
    print(f"📊 Insurance Coverage: {stats['insurance_coverage_percentage']:.1f}%")
    
    print("\n📊 Age Distribution:")
    for age_group, count in stats['age_distribution'].items():
        percentage = (count / stats['total_patients'] * 100) if stats['total_patients'] > 0 else 0
        print(f"  {age_group}: {count} patients ({percentage:.1f}%)")
        
    return stats

def generate_appointment_report():
    """Generate appointment analytics"""
    print("\n📅 Generating Appointment Analytics...")
    
    appointment_service = AppointmentService()
    stats = appointment_service.get_appointment_statistics()
    
    print(f"📈 Total Appointments: {stats['total_appointments']}")
    print(f"⏰ Upcoming Appointments: {stats['upcoming_appointments']}")
    print(f"⚠️  Overdue Appointments: {stats['overdue_appointments']}")
    
    print("\n📊 Appointment Status Distribution:")
    for status, count in stats['status_distribution'].items():
        percentage = (count / stats['total_appointments'] * 100) if stats['total_appointments'] > 0 else 0
        print(f"  {status.title()}: {count} ({percentage:.1f}%)")
        
    print("\n📊 Appointment Type Distribution:")
    for app_type, count in stats['type_distribution'].items():
        percentage = (count / stats['total_appointments'] * 100) if stats['total_appointments'] > 0 else 0
        print(f"  {app_type.title()}: {count} ({percentage:.1f}%)")
        
    return stats

def generate_revenue_report():
    """Generate revenue analytics"""
    print("\n💰 Generating Revenue Analytics...")
    
    billing_service = BillingService()
    stats = billing_service.get_billing_statistics()
    
    print(f"📈 Total Revenue: ${stats['total_billed']:,.2f}")
    print(f"💳 Total Paid: ${stats['total_paid']:,.2f}")
    print(f"📊 Outstanding Balance: ${stats['total_outstanding']:,.2f}")
    print(f"📈 Collection Rate: {stats['collection_rate']:.1f}%")
    print(f"📄 Total Invoices: {stats['total_invoices']}")
    print(f"📋 Total Claims: {stats['total_claims']}")
    print(f"⚠️  Overdue Invoices: {stats['overdue_invoices']}")
    
    print("\n📊 Invoice Status Distribution:")
    for status, count in stats['invoice_status_distribution'].items():
        percentage = (count / stats['total_invoices'] * 100) if stats['total_invoices'] > 0 else 0
        print(f"  {status.title()}: {count} ({percentage:.1f}%)")
        
    return stats

def generate_kpi_report():
    """Generate key performance indicators"""
    print("\n🎯 Generating Key Performance Indicators...")
    
    analytics = AnalyticsEngine()
    kpis = analytics.get_key_performance_indicators()
    
    print("📊 Key Performance Indicators:")
    print(f"  👥 Total Patients: {kpis['kpis']['total_patients']}")
    print(f"  💰 Total Revenue: ${kpis['kpis']['total_revenue']:,.2f}")
    print(f"  📈 Collection Rate: {kpis['kpis']['collection_rate']:.1f}%")
    print(f"  ✅ Completion Rate: {kpis['kpis']['completion_rate']:.1f}%")
    print(f"  🔄 Patient Retention Rate: {kpis['kpis']['patient_retention_rate']:.1f}%")
    print(f"  💵 Average Invoice Amount: ${kpis['kpis']['average_invoice_amount']:.2f}")
    
    return kpis

def generate_monthly_trends():
    """Generate monthly trend analysis"""
    print("\n📈 Generating Monthly Trends...")
    
    analytics = AnalyticsEngine()
    
    # Get revenue trends
    revenue_data = analytics.generate_revenue_analytics()
    revenue_trends = revenue_data.get('revenue_analysis', {}).get('revenue_by_month', {})
    
    print("💰 Monthly Revenue Trends:")
    for month, revenue in sorted(revenue_trends.items()):
        print(f"  {month}: ${revenue:,.2f}")
        
    # Get appointment trends
    appointment_data = analytics.generate_appointment_analytics()
    appointment_trends = appointment_data.get('appointment_trends', {}).get('by_month', {})
    
    print("\n📅 Monthly Appointment Trends:")
    for month, count in sorted(appointment_trends.items()):
        print(f"  {month}: {count} appointments")
        
    return {
        'revenue_trends': revenue_trends,
        'appointment_trends': appointment_trends
    }

def generate_insurance_analysis():
    """Generate insurance provider analysis"""
    print("\n🏥 Generating Insurance Provider Analysis...")
    
    patient_service = PatientService()
    patients = patient_service.get_all_patients()
    
    insurance_counts = {}
    for patient in patients:
        if patient.insurance_provider:
            insurance_counts[patient.insurance_provider] = insurance_counts.get(patient.insurance_provider, 0) + 1
            
    total_patients = len(patients)
    
    print("📊 Insurance Provider Distribution:")
    for provider, count in sorted(insurance_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_patients * 100) if total_patients > 0 else 0
        print(f"  {provider}: {count} patients ({percentage:.1f}%)")
        
    return insurance_counts

def generate_service_analysis():
    """Generate service type analysis"""
    print("\n🦷 Generating Service Type Analysis...")
    
    appointment_service = AppointmentService()
    appointments = list(appointment_service.appointments.values())
    
    service_counts = {}
    for appointment in appointments:
        service_type = appointment.appointment_type.value
        service_counts[service_type] = service_counts.get(service_type, 0) + 1
        
    total_appointments = len(appointments)
    
    print("📊 Service Type Distribution:")
    for service, count in sorted(service_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_appointments * 100) if total_appointments > 0 else 0
        print(f"  {service.title()}: {count} appointments ({percentage:.1f}%)")
        
    return service_counts

def generate_operational_metrics():
    """Generate operational efficiency metrics"""
    print("\n⚙️ Generating Operational Metrics...")
    
    appointment_service = AppointmentService()
    appointments = list(appointment_service.appointments.values())
    
    # Calculate operational metrics
    total_appointments = len(appointments)
    completed_appointments = len([a for a in appointments if a.status.value == 'completed'])
    cancelled_appointments = len([a for a in appointments if a.status.value == 'cancelled'])
    
    completion_rate = (completed_appointments / total_appointments * 100) if total_appointments > 0 else 0
    cancellation_rate = (cancelled_appointments / total_appointments * 100) if total_appointments > 0 else 0
    
    print(f"📈 Completion Rate: {completion_rate:.1f}%")
    print(f"❌ Cancellation Rate: {cancellation_rate:.1f}%")
    print(f"✅ Completed Appointments: {completed_appointments}")
    print(f"❌ Cancelled Appointments: {cancelled_appointments}")
    
    return {
        'completion_rate': completion_rate,
        'cancellation_rate': cancellation_rate,
        'completed_appointments': completed_appointments,
        'cancelled_appointments': cancelled_appointments
    }

def export_report_to_markdown(report_data: Dict, filename: str = None):
    """Export report to Markdown format"""
    if not filename:
        filename = f"dental_practice_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
    os.makedirs("reports", exist_ok=True)
    filepath = os.path.join("reports", filename)
    
    with open(filepath, 'w') as f:
        f.write("# Dental Practice Analytics Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n\n")
        
        # Practice Overview
        f.write("## Practice Overview\n\n")
        practice_data = report_data.get('practice_overview', {})
        if practice_data:
            overview = practice_data.get('practice_overview', {})
            f.write(f"- **Total Patients:** {overview.get('total_patients', 0)}\n")
            f.write(f"- **Total Appointments:** {overview.get('total_appointments', 0)}\n")
            f.write(f"- **Total Revenue:** ${overview.get('total_revenue', 0):,.2f}\n")
            f.write(f"- **Collection Rate:** {overview.get('collection_rate', 0):.1f}%\n\n")
            
        # KPIs
        f.write("## Key Performance Indicators\n\n")
        kpis = report_data.get('kpis', {})
        if kpis:
            kpi_data = kpis.get('kpis', {})
            f.write(f"- **Total Patients:** {kpi_data.get('total_patients', 0)}\n")
            f.write(f"- **Total Revenue:** ${kpi_data.get('total_revenue', 0):,.2f}\n")
            f.write(f"- **Collection Rate:** {kpi_data.get('collection_rate', 0):.1f}%\n")
            f.write(f"- **Completion Rate:** {kpi_data.get('completion_rate', 0):.1f}%\n")
            f.write(f"- **Patient Retention Rate:** {kpi_data.get('patient_retention_rate', 0):.1f}%\n")
            f.write(f"- **Average Invoice Amount:** ${kpi_data.get('average_invoice_amount', 0):.2f}\n\n")
            
    print(f"✅ Markdown report exported to: {filepath}")
    return filepath

def main():
    """Main function to generate all reports"""
    print("🚀 Generating Comprehensive Dental Practice Analytics...")
    print("=" * 60)
    
    try:
        # Generate all reports
        practice_report = generate_practice_report()
        patient_stats = generate_patient_report()
        appointment_stats = generate_appointment_report()
        revenue_stats = generate_revenue_report()
        kpi_stats = generate_kpi_report()
        monthly_trends = generate_monthly_trends()
        insurance_analysis = generate_insurance_analysis()
        service_analysis = generate_service_analysis()
        operational_metrics = generate_operational_metrics()
        
        # Combine all data
        comprehensive_report = {
            'practice_overview': practice_report,
            'patient_analytics': patient_stats,
            'appointment_analytics': appointment_stats,
            'revenue_analytics': revenue_stats,
            'kpis': kpi_stats,
            'monthly_trends': monthly_trends,
            'insurance_analysis': insurance_analysis,
            'service_analysis': service_analysis,
            'operational_metrics': operational_metrics
        }
        
        # Export to Markdown
        markdown_file = export_report_to_markdown(comprehensive_report)
        
        print("\n" + "=" * 60)
        print("✅ Analytics Report Generation Completed!")
        print(f"📄 Reports saved to: reports/")
        print(f"📊 Markdown report: {markdown_file}")
        print("\n🎉 Your dental practice analytics are ready!")
        
    except Exception as e:
        print(f"\n❌ Error during report generation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
