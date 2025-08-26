# Dental Voice Agent API Documentation

## Overview

The Dental Voice Agent API provides comprehensive endpoints for managing a dental practice, including patient management, appointment scheduling, billing, and voice assistant functionality.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication for development purposes. In production, implement proper authentication mechanisms.

## Response Format

All API responses follow a consistent format:

```json
{
  "success": true|false,
  "data": {...},
  "message": "Optional message",
  "error": "Error description if success is false"
}
```

## Endpoints

### Voice Assistant API

#### Process Voice Query

**POST** `/api/voice/process`

Process a voice or text query and return an AI-generated response.

**Request Body:**
```json
{
  "query": "I want to schedule an appointment"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "original_text": "I want to schedule an appointment",
    "intent": "schedule_appointment",
    "entities": {
      "preferred_time": "tomorrow",
      "service_type": "cleaning"
    },
    "response": "I'd be happy to help you schedule a cleaning appointment..."
  }
}
```

### Patient Management API

#### Get All Patients

**GET** `/api/patients/`

Retrieve all patients with optional filtering and pagination.

**Query Parameters:**
- `search` (string): Search patients by name, email, or phone
- `insurance_provider` (string): Filter by insurance provider
- `limit` (integer): Number of results per page (default: 50)
- `offset` (integer): Number of results to skip (default: 0)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "patient_id": "P0001",
      "first_name": "John",
      "last_name": "Smith",
      "email": "john.smith@email.com",
      "phone": "(555) 123-4567",
      "date_of_birth": "1985-03-15",
      "insurance_provider": "Delta Dental",
      "insurance_id": "DD123456789",
      "created_at": "2023-01-15T10:30:00",
      "updated_at": "2023-01-15T10:30:00"
    }
  ],
  "pagination": {
    "total": 100,
    "limit": 50,
    "offset": 0,
    "has_more": true
  }
}
```

#### Get Patient by ID

**GET** `/api/patients/{patient_id}`

Retrieve a specific patient by their ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "patient_id": "P0001",
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@email.com",
    "phone": "(555) 123-4567",
    "date_of_birth": "1985-03-15",
    "insurance_provider": "Delta Dental",
    "insurance_id": "DD123456789",
    "medical_history": [...],
    "treatments": [...],
    "notes": [...]
  }
}
```

#### Create Patient

**POST** `/api/patients/`

Create a new patient record.

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@email.com",
  "phone": "(555) 987-6543",
  "date_of_birth": "1990-07-22",
  "insurance_provider": "Aetna",
  "insurance_id": "AE987654321"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "patient_id": "P0002",
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@email.com",
    "phone": "(555) 987-6543",
    "date_of_birth": "1990-07-22",
    "insurance_provider": "Aetna",
    "insurance_id": "AE987654321",
    "created_at": "2023-01-15T11:00:00",
    "updated_at": "2023-01-15T11:00:00"
  },
  "message": "Patient created successfully"
}
```

#### Update Patient

**PUT** `/api/patients/{patient_id}`

Update an existing patient record.

**Request Body:**
```json
{
  "phone": "(555) 111-2222",
  "insurance_provider": "Cigna"
}
```

#### Delete Patient

**DELETE** `/api/patients/{patient_id}`

Delete a patient record.

#### Search Patients

**GET** `/api/patients/search?q={query}`

Search patients by name, email, or phone number.

#### Get Patient Statistics

**GET** `/api/patients/statistics`

Get patient demographics and statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_patients": 150,
    "patients_with_insurance": 120,
    "insurance_coverage_percentage": 80.0,
    "age_distribution": {
      "0-17": 15,
      "18-30": 25,
      "31-50": 45,
      "51-70": 35,
      "70+": 30
    }
  }
}
```

### Appointment Management API

#### Get All Appointments

**GET** `/api/appointments/`

Retrieve all appointments with optional filtering.

**Query Parameters:**
- `patient_id` (string): Filter by patient ID
- `dentist_id` (string): Filter by dentist ID
- `status` (string): Filter by appointment status
- `date` (string): Filter by date (YYYY-MM-DD)
- `limit` (integer): Number of results per page
- `offset` (integer): Number of results to skip

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "appointment_id": "A0001",
      "patient_id": "P0001",
      "appointment_type": "cleaning",
      "scheduled_date": "2023-01-20T10:00:00",
      "duration_minutes": 60,
      "dentist_id": "D0001",
      "status": "scheduled",
      "notes": "Regular cleaning appointment"
    }
  ],
  "pagination": {
    "total": 50,
    "limit": 50,
    "offset": 0,
    "has_more": false
  }
}
```

#### Get Appointment by ID

**GET** `/api/appointments/{appointment_id}`

Retrieve a specific appointment by ID.

#### Create Appointment

**POST** `/api/appointments/`

Create a new appointment.

**Request Body:**
```json
{
  "patient_id": "P0001",
  "appointment_type": "cleaning",
  "scheduled_date": "2023-01-20T10:00:00",
  "duration_minutes": 60,
  "dentist_id": "D0001",
  "notes": "Regular cleaning appointment"
}
```

#### Update Appointment

**PUT** `/api/appointments/{appointment_id}`

Update an existing appointment.

**Request Body:**
```json
{
  "status": "confirmed",
  "scheduled_date": "2023-01-20T11:00:00"
}
```

#### Cancel Appointment

**DELETE** `/api/appointments/{appointment_id}`

Cancel an appointment.

**Request Body:**
```json
{
  "reason": "Patient requested cancellation"
}
```

#### Get Available Slots

**GET** `/api/appointments/available-slots`

Get available appointment slots for a specific date.

**Query Parameters:**
- `date` (string): Date in YYYY-MM-DD format (required)
- `duration` (integer): Appointment duration in minutes (default: 60)
- `dentist_id` (string): Filter by specific dentist

**Response:**
```json
{
  "success": true,
  "data": {
    "date": "2023-01-20",
    "duration_minutes": 60,
    "available_slots": [
      "2023-01-20T09:00:00",
      "2023-01-20T10:00:00",
      "2023-01-20T14:00:00"
    ],
    "count": 3
  }
}
```

#### Get Upcoming Appointments

**GET** `/api/appointments/upcoming`

Get upcoming appointments within a specified time frame.

**Query Parameters:**
- `hours` (integer): Hours ahead to look (default: 24)

#### Get Overdue Appointments

**GET** `/api/appointments/overdue`

Get appointments that are overdue.

#### Get Appointment Statistics

**GET** `/api/appointments/statistics`

Get appointment statistics and analytics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_appointments": 150,
    "status_distribution": {
      "scheduled": 45,
      "confirmed": 30,
      "completed": 60,
      "cancelled": 10,
      "no_show": 5
    },
    "type_distribution": {
      "consultation": 20,
      "cleaning": 50,
      "filling": 30,
      "root_canal": 10,
      "whitening": 15,
      "emergency": 25
    },
    "upcoming_appointments": 8,
    "overdue_appointments": 2
  }
}
```

### Billing API

#### Get All Invoices

**GET** `/api/billing/invoices`

Retrieve all invoices with optional filtering.

**Query Parameters:**
- `patient_id` (string): Filter by patient ID
- `status` (string): Filter by invoice status
- `limit` (integer): Number of results per page
- `offset` (integer): Number of results to skip

#### Get Invoice by ID

**GET** `/api/billing/invoices/{invoice_id}`

Retrieve a specific invoice by ID.

#### Create Invoice

**POST** `/api/billing/invoices`

Create a new invoice.

**Request Body:**
```json
{
  "patient_id": "P0001",
  "appointment_id": "A0001",
  "items": [
    {
      "description": "Teeth Cleaning",
      "quantity": 1,
      "unit_price": 120.00
    }
  ]
}
```

#### Record Payment

**POST** `/api/billing/invoices/{invoice_id}/payments`

Record a payment for an invoice.

**Request Body:**
```json
{
  "amount": 120.00,
  "payment_method": "credit_card",
  "reference": "CC123456",
  "notes": "Payment received"
}
```

#### Get Billing Statistics

**GET** `/api/billing/statistics`

Get billing and financial statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_invoices": 100,
    "total_billed": 25000.00,
    "total_paid": 22000.00,
    "total_outstanding": 3000.00,
    "collection_rate": 88.0,
    "invoice_status_distribution": {
      "paid": 80,
      "pending": 15,
      "overdue": 5
    }
  }
}
```

### Dashboard API

#### Get Dashboard Statistics

**GET** `/api/dashboard/statistics`

Get comprehensive dashboard statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_patients": 150,
    "today_appointments": 8,
    "monthly_revenue": 25000.00,
    "pending_appointments": 12,
    "completion_rate": 85.0,
    "patient_retention_rate": 78.0
  }
}
```

#### Get Appointment Trends

**GET** `/api/dashboard/appointments`

Get appointment trends for charting.

**Query Parameters:**
- `days` (integer): Number of days to include (default: 30)

**Response:**
```json
{
  "success": true,
  "data": {
    "labels": ["2023-01-01", "2023-01-02", "2023-01-03"],
    "values": [5, 8, 3]
  }
}
```

#### Get Revenue Trends

**GET** `/api/dashboard/revenue`

Get revenue trends for charting.

**Query Parameters:**
- `days` (integer): Number of days to include (default: 30)

**Response:**
```json
{
  "success": true,
  "data": {
    "labels": ["2023-01-01", "2023-01-02", "2023-01-03"],
    "values": [1200.00, 1800.00, 900.00]
  }
}
```

### Notification API

#### Send Appointment Reminder

**POST** `/api/notifications/appointment-reminder`

Send appointment reminder notifications.

**Request Body:**
```json
{
  "patient_id": "P0001",
  "appointment_id": "A0001",
  "appointment_date": "2023-01-20T10:00:00",
  "patient_email": "john.smith@email.com",
  "patient_phone": "(555) 123-4567"
}
```

#### Send Payment Reminder

**POST** `/api/notifications/payment-reminder`

Send payment reminder notifications.

**Request Body:**
```json
{
  "patient_id": "P0001",
  "invoice_id": "INV0001",
  "amount": 120.00,
  "due_date": "2023-01-25T00:00:00",
  "patient_email": "john.smith@email.com"
}
```

#### Get Notification Statistics

**GET** `/api/notifications/statistics`

Get notification delivery statistics.

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input data |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource conflict (e.g., appointment time slot unavailable) |
| 500 | Internal Server Error |

## Rate Limiting

Currently, no rate limiting is implemented. In production, implement appropriate rate limiting based on your requirements.

## CORS

The API supports CORS for cross-origin requests. Configure CORS settings in production based on your frontend domain.

## Data Formats

### Dates and Times

All dates and times are in ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`

### Currency

All monetary values are in USD and represented as decimal numbers (e.g., 120.50 for $120.50).

### IDs

All IDs are strings and follow these patterns:
- Patient IDs: `P` + 4-digit number (e.g., `P0001`)
- Appointment IDs: `A` + 4-digit number (e.g., `A0001`)
- Invoice IDs: `INV` + 4-digit number (e.g., `INV0001`)

## Examples

### Complete Workflow Example

1. **Create a patient:**
```bash
curl -X POST http://localhost:5000/api/patients/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@email.com",
    "phone": "(555) 123-4567",
    "date_of_birth": "1985-03-15"
  }'
```

2. **Schedule an appointment:**
```bash
curl -X POST http://localhost:5000/api/appointments/ \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P0001",
    "appointment_type": "cleaning",
    "scheduled_date": "2023-01-20T10:00:00",
    "duration_minutes": 60
  }'
```

3. **Create an invoice:**
```bash
curl -X POST http://localhost:5000/api/billing/invoices \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "P0001",
    "appointment_id": "A0001",
    "items": [
      {
        "description": "Teeth Cleaning",
        "quantity": 1,
        "unit_price": 120.00
      }
    ]
  }'
```

4. **Process a voice query:**
```bash
curl -X POST http://localhost:5000/api/voice/process \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are your office hours?"
  }'
```

## Testing

Use the provided test scripts to verify API functionality:

```bash
# Run unit tests
python -m pytest tests/

# Run specific test file
python tests/test_voice_processor.py

# Test API endpoints
python test_api.py
```

## Support

For API support and questions, please refer to the project documentation or create an issue in the project repository.
