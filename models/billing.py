from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
import uuid

class PaymentStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    PARTIAL = "partial"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class PaymentMethod(Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CHECK = "check"
    INSURANCE = "insurance"
    ONLINE = "online"

class InvoiceStatus(Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class BillingItem:
    def __init__(self, item_id: str, description: str, quantity: int, 
                 unit_price: float, service_code: Optional[str] = None):
        self.item_id = item_id
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
        self.service_code = service_code
        self.total = quantity * unit_price
        
    def to_dict(self) -> Dict:
        return {
            'item_id': self.item_id,
            'description': self.description,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'service_code': self.service_code,
            'total': self.total
        }

class Invoice:
    def __init__(self, invoice_id: str, patient_id: str, appointment_id: Optional[str] = None):
        self.invoice_id = invoice_id
        self.patient_id = patient_id
        self.appointment_id = appointment_id
        self.created_date = datetime.now()
        self.due_date = datetime.now()
        self.status = InvoiceStatus.DRAFT
        self.items = []
        self.subtotal = 0.0
        self.tax_rate = 0.08  # 8% tax rate
        self.tax_amount = 0.0
        self.total_amount = 0.0
        self.paid_amount = 0.0
        self.balance_due = 0.0
        self.notes = ""
        self.insurance_info = None
        
    def add_item(self, item: BillingItem):
        self.items.append(item)
        self._recalculate_totals()
        
    def remove_item(self, item_id: str):
        self.items = [item for item in self.items if item.item_id != item_id]
        self._recalculate_totals()
        
    def _recalculate_totals(self):
        self.subtotal = sum(item.total for item in self.items)
        self.tax_amount = self.subtotal * self.tax_rate
        self.total_amount = self.subtotal + self.tax_amount
        self.balance_due = self.total_amount - self.paid_amount
        
    def add_payment(self, amount: float, payment_method: PaymentMethod, 
                   reference: str = "", notes: str = ""):
        payment = {
            'payment_id': str(uuid.uuid4()),
            'amount': amount,
            'payment_method': payment_method.value,
            'reference': reference,
            'notes': notes,
            'date': datetime.now().isoformat()
        }
        self.paid_amount += amount
        self.balance_due = self.total_amount - self.paid_amount
        
        if self.balance_due <= 0:
            self.status = InvoiceStatus.PAID
        elif self.balance_due < self.total_amount:
            self.status = InvoiceStatus.PARTIAL
            
        return payment
        
    def set_insurance_info(self, provider: str, policy_number: str, 
                          group_number: str = "", coverage_percentage: float = 0.0):
        self.insurance_info = {
            'provider': provider,
            'policy_number': policy_number,
            'group_number': group_number,
            'coverage_percentage': coverage_percentage
        }
        
    def to_dict(self) -> Dict:
        return {
            'invoice_id': self.invoice_id,
            'patient_id': self.patient_id,
            'appointment_id': self.appointment_id,
            'created_date': self.created_date.isoformat(),
            'due_date': self.due_date.isoformat(),
            'status': self.status.value,
            'items': [item.to_dict() for item in self.items],
            'subtotal': self.subtotal,
            'tax_rate': self.tax_rate,
            'tax_amount': self.tax_amount,
            'total_amount': self.total_amount,
            'paid_amount': self.paid_amount,
            'balance_due': self.balance_due,
            'notes': self.notes,
            'insurance_info': self.insurance_info
        }
        
    def is_overdue(self) -> bool:
        return datetime.now() > self.due_date and self.balance_due > 0
        
    def get_payment_status(self) -> PaymentStatus:
        if self.balance_due <= 0:
            return PaymentStatus.PAID
        elif self.paid_amount > 0:
            return PaymentStatus.PARTIAL
        elif self.is_overdue():
            return PaymentStatus.OVERDUE
        else:
            return PaymentStatus.PENDING

class InsuranceClaim:
    def __init__(self, claim_id: str, patient_id: str, invoice_id: str,
                 insurance_provider: str, policy_number: str):
        self.claim_id = claim_id
        self.patient_id = patient_id
        self.invoice_id = invoice_id
        self.insurance_provider = insurance_provider
        self.policy_number = policy_number
        self.submitted_date = datetime.now()
        self.status = "submitted"
        self.claim_amount = 0.0
        self.approved_amount = 0.0
        self.denied_amount = 0.0
        self.response_date = None
        self.notes = ""
        
    def to_dict(self) -> Dict:
        return {
            'claim_id': self.claim_id,
            'patient_id': self.patient_id,
            'invoice_id': self.invoice_id,
            'insurance_provider': self.insurance_provider,
            'policy_number': self.policy_number,
            'submitted_date': self.submitted_date.isoformat(),
            'status': self.status,
            'claim_amount': self.claim_amount,
            'approved_amount': self.approved_amount,
            'denied_amount': self.denied_amount,
            'response_date': self.response_date.isoformat() if self.response_date else None,
            'notes': self.notes
        }
