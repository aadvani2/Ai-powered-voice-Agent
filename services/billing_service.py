from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
import os
from models.billing import Invoice, BillingItem, InsuranceClaim, PaymentMethod, PaymentStatus, InvoiceStatus

class BillingService:
    def __init__(self, data_file: str = "data/billing.json"):
        self.data_file = data_file
        self.invoices = {}
        self.insurance_claims = {}
        self._load_billing_data()
        
    def _load_billing_data(self):
        """Load billing data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    # Load invoices
                    for invoice_data in data.get('invoices', {}).values():
                        invoice = self._create_invoice_from_dict(invoice_data)
                        self.invoices[invoice.invoice_id] = invoice
                    # Load insurance claims
                    for claim_data in data.get('insurance_claims', {}).values():
                        claim = self._create_claim_from_dict(claim_data)
                        self.insurance_claims[claim.claim_id] = claim
            except Exception as e:
                print(f"Error loading billing data: {e}")
                
    def _save_billing_data(self):
        """Save billing data to JSON file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        try:
            data = {
                'invoices': {iid: invoice.to_dict() for iid, invoice in self.invoices.items()},
                'insurance_claims': {cid: claim.to_dict() for cid, claim in self.insurance_claims.items()}
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving billing data: {e}")
            
    def _create_invoice_from_dict(self, data: Dict) -> Invoice:
        """Create an Invoice object from dictionary data"""
        invoice = Invoice(
            invoice_id=data['invoice_id'],
            patient_id=data['patient_id'],
            appointment_id=data.get('appointment_id')
        )
        
        # Restore additional data
        invoice.created_date = datetime.fromisoformat(data['created_date'])
        invoice.due_date = datetime.fromisoformat(data['due_date'])
        invoice.status = InvoiceStatus(data['status'])
        invoice.subtotal = data['subtotal']
        invoice.tax_rate = data['tax_rate']
        invoice.tax_amount = data['tax_amount']
        invoice.total_amount = data['total_amount']
        invoice.paid_amount = data['paid_amount']
        invoice.balance_due = data['balance_due']
        invoice.notes = data.get('notes', '')
        invoice.insurance_info = data.get('insurance_info')
        
        # Restore items
        for item_data in data.get('items', []):
            item = BillingItem(
                item_id=item_data['item_id'],
                description=item_data['description'],
                quantity=item_data['quantity'],
                unit_price=item_data['unit_price'],
                service_code=item_data.get('service_code')
            )
            invoice.items.append(item)
            
        return invoice
        
    def _create_claim_from_dict(self, data: Dict) -> InsuranceClaim:
        """Create an InsuranceClaim object from dictionary data"""
        claim = InsuranceClaim(
            claim_id=data['claim_id'],
            patient_id=data['patient_id'],
            invoice_id=data['invoice_id'],
            insurance_provider=data['insurance_provider'],
            policy_number=data['policy_number']
        )
        
        # Restore additional data
        claim.submitted_date = datetime.fromisoformat(data['submitted_date'])
        claim.status = data['status']
        claim.claim_amount = data['claim_amount']
        claim.approved_amount = data['approved_amount']
        claim.denied_amount = data['denied_amount']
        claim.response_date = datetime.fromisoformat(data['response_date']) if data.get('response_date') else None
        claim.notes = data.get('notes', '')
        
        return claim
        
    def create_invoice(self, patient_id: str, appointment_id: Optional[str] = None) -> Invoice:
        """Create a new invoice"""
        invoice_id = f"INV{len(self.invoices) + 1:04d}"
        invoice = Invoice(
            invoice_id=invoice_id,
            patient_id=patient_id,
            appointment_id=appointment_id
        )
        
        # Set due date to 30 days from now
        invoice.due_date = datetime.now() + timedelta(days=30)
        
        self.invoices[invoice_id] = invoice
        self._save_billing_data()
        return invoice
        
    def add_invoice_item(self, invoice_id: str, description: str, quantity: int,
                        unit_price: float, service_code: Optional[str] = None) -> bool:
        """Add item to invoice"""
        invoice = self.get_invoice(invoice_id)
        if not invoice:
            return False
            
        item_id = f"ITEM{len(invoice.items) + 1:03d}"
        item = BillingItem(
            item_id=item_id,
            description=description,
            quantity=quantity,
            unit_price=unit_price,
            service_code=service_code
        )
        
        invoice.add_item(item)
        self._save_billing_data()
        return True
        
    def get_invoice(self, invoice_id: str) -> Optional[Invoice]:
        """Get invoice by ID"""
        return self.invoices.get(invoice_id)
        
    def get_invoices_by_patient(self, patient_id: str) -> List[Invoice]:
        """Get all invoices for a patient"""
        return [inv for inv in self.invoices.values() if inv.patient_id == patient_id]
        
    def get_invoices_by_status(self, status: InvoiceStatus) -> List[Invoice]:
        """Get invoices by status"""
        return [inv for inv in self.invoices.values() if inv.status == status]
        
    def get_overdue_invoices(self) -> List[Invoice]:
        """Get overdue invoices"""
        return [inv for inv in self.invoices.values() if inv.is_overdue()]
        
    def record_payment(self, invoice_id: str, amount: float, payment_method: PaymentMethod,
                      reference: str = "", notes: str = "") -> bool:
        """Record a payment for an invoice"""
        invoice = self.get_invoice(invoice_id)
        if not invoice:
            return False
            
        payment = invoice.add_payment(amount, payment_method, reference, notes)
        self._save_billing_data()
        return True
        
    def set_insurance_info(self, invoice_id: str, provider: str, policy_number: str,
                          group_number: str = "", coverage_percentage: float = 0.0) -> bool:
        """Set insurance information for an invoice"""
        invoice = self.get_invoice(invoice_id)
        if not invoice:
            return False
            
        invoice.set_insurance_info(provider, policy_number, group_number, coverage_percentage)
        self._save_billing_data()
        return True
        
    def create_insurance_claim(self, patient_id: str, invoice_id: str,
                              insurance_provider: str, policy_number: str) -> InsuranceClaim:
        """Create a new insurance claim"""
        claim_id = f"CLM{len(self.insurance_claims) + 1:04d}"
        claim = InsuranceClaim(
            claim_id=claim_id,
            patient_id=patient_id,
            invoice_id=invoice_id,
            insurance_provider=insurance_provider,
            policy_number=policy_number
        )
        
        # Set claim amount from invoice
        invoice = self.get_invoice(invoice_id)
        if invoice:
            claim.claim_amount = invoice.total_amount
            
        self.insurance_claims[claim_id] = claim
        self._save_billing_data()
        return claim
        
    def get_claim(self, claim_id: str) -> Optional[InsuranceClaim]:
        """Get insurance claim by ID"""
        return self.insurance_claims.get(claim_id)
        
    def get_claims_by_patient(self, patient_id: str) -> List[InsuranceClaim]:
        """Get all claims for a patient"""
        return [claim for claim in self.insurance_claims.values() if claim.patient_id == patient_id]
        
    def get_claims_by_status(self, status: str) -> List[InsuranceClaim]:
        """Get claims by status"""
        return [claim for claim in self.insurance_claims.values() if claim.status == status]
        
    def update_claim_status(self, claim_id: str, status: str, approved_amount: float = 0.0,
                          denied_amount: float = 0.0, notes: str = "") -> bool:
        """Update insurance claim status"""
        claim = self.get_claim(claim_id)
        if not claim:
            return False
            
        claim.status = status
        claim.approved_amount = approved_amount
        claim.denied_amount = denied_amount
        claim.notes = notes
        claim.response_date = datetime.now()
        
        self._save_billing_data()
        return True
        
    def get_billing_statistics(self) -> Dict:
        """Get billing statistics"""
        total_invoices = len(self.invoices)
        total_claims = len(self.insurance_claims)
        
        # Calculate totals
        total_billed = sum(inv.total_amount for inv in self.invoices.values())
        total_paid = sum(inv.paid_amount for inv in self.invoices.values())
        total_outstanding = sum(inv.balance_due for inv in self.invoices.values())
        
        # Status distribution
        status_counts = {}
        for status in InvoiceStatus:
            status_counts[status.value] = len(self.get_invoices_by_status(status))
            
        # Claims status
        claim_status_counts = {}
        for claim in self.insurance_claims.values():
            status = claim.status
            claim_status_counts[status] = claim_status_counts.get(status, 0) + 1
            
        return {
            "total_invoices": total_invoices,
            "total_claims": total_claims,
            "total_billed": total_billed,
            "total_paid": total_paid,
            "total_outstanding": total_outstanding,
            "collection_rate": (total_paid / total_billed * 100) if total_billed > 0 else 0,
            "invoice_status_distribution": status_counts,
            "claim_status_distribution": claim_status_counts,
            "overdue_invoices": len(self.get_overdue_invoices())
        }
