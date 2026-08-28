# Modular Receipt Verification Engine — V1

A backend service for validating and verifying structured financial transaction data against a PostgreSQL database.

The first version focuses deliberately on the **core verification engine** rather than OCR, PDF processing, Telegram integration, or external banking APIs.

The goal of V1 is to build a reliable and modular backend that can receive transaction data through an API, validate it, check the database, detect duplicates, and return a standardized verification result.

---

## Project Goal

The system is designed around a simple principle:

> Build the verification engine independently from the interface used to interact with it.

For V1, the interface is a **FastAPI HTTP API**.

In future versions, other interfaces such as Telegram, OCR, PDF processing, and external verification providers can be connected to the same core engine without rewriting the verification logic.

### V1 Architecture

```text
                    ┌──────────────────┐
                    │    API Client    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     FastAPI      │
                    │   API Interface  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Verification    │
                    │     Service      │
                    └────────┬─────────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
        ┌─────────────────┐    ┌─────────────────┐
        │    Validation   │    │   PostgreSQL    │
        │     Rules       │    │    Database     │
        └─────────────────┘    └─────────────────┘
                 │                       │
                 └───────────┬───────────┘
                             ▼
                    ┌──────────────────┐
                    │ Verification     │
                    │     Result       │
                    └──────────────────┘
```

---

# V1 Scope

V1 intentionally focuses on structured transaction data.

### Included in V1

* FastAPI API
* Pydantic request/response schemas
* PostgreSQL database
* SQLModel/SQLAlchemy database layer
* Transaction data validation
* Transaction lookup
* Duplicate detection
* Verification logic
* Standardized verification results
* Error handling
* Unit tests
* API/integration tests

### Not included in V1

The following are planned for later versions:

* OCR
* Image processing
* PDF processing
* Telegram bot
* External bank APIs
* Multiple bank-specific OCR parsers
* Production-scale asynchronous processing
* Advanced monitoring
* CLI interface

These features will be implemented as additional layers around the V1 core rather than being tightly coupled to the verification logic.

---

# Core Workflow

A V1 verification request follows this process:

```text
Client
  │
  │ POST /verify
  ▼
FastAPI
  │
  ▼
Request Validation
  │
  ▼
Verification Service
  │
  ├── Validate transaction
  │
  ├── Search database
  │
  ├── Check duplicate
  │
  └── Determine result
  │
  ▼
VerificationResult
  │
  ▼
API Response
```

---

# Example Request

```http
POST /verify
Content-Type: application/json
```

```json
{
  "bank": "cbe",
  "amount": "1500.00",
  "transaction_reference": "TX123456",
  "sender": "Abebe",
  "receiver": "Yisak",
  "transaction_date": "2026-08-28T10:30:00"
}
```

# Example Response

### Verified Transaction

```json
{
  "status": "verified",
  "transaction_reference": "TX123456",
  "message": "Transaction verified"
}
```

### Duplicate Transaction

```json
{
  "status": "duplicate",
  "transaction_reference": "TX123456",
  "message": "Transaction has already been processed"
}
```

### Invalid Transaction

```json
{
  "status": "invalid",
  "transaction_reference": "TX123456",
  "message": "Invalid transaction data"
}
```

---

# Verification States

The V1 engine uses explicit verification states.

| Status      | Meaning                                                                   |
| ----------- | ------------------------------------------------------------------------- |
| `verified`  | Transaction is valid and has been successfully verified                   |
| `duplicate` | Transaction has already been processed                                    |
| `invalid`   | Transaction data fails validation                                         |
| `failed`    | Verification could not be completed because of an internal/system failure |

Keeping these states standardized allows future interfaces to consume the same result.

For example:

```text
                    VerificationResult
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           FastAPI      Telegram       CLI
```

The interface does not need to know how verification works internally.

---

# Project Structure

The project is organized to keep the API, business logic, and database code separated.

```text
src/
│
├── api/
│   ├── routes/
│   │   └── verification.py
│   └── schemas/
│       └── verification.py
│
├── core/
│   └── verifier.py
│
├── db/
│   ├── models.py
│   ├── main.py
│   └── repository.py
│
└── main.py

tests/
│
├── unit/
│   ├── test_verifier.py
│   └── test_schemas.py
│
└── integration/
    ├── test_database.py
    └── test_api.py
```

The exact structure may evolve as the project develops.

---

# Main Components

## FastAPI

FastAPI provides the HTTP interface for interacting with the verification engine.

Its responsibility is primarily to:

1. Receive requests
2. Validate request schemas
3. Pass data to the verification service
4. Return verification results
5. Handle HTTP-level errors

The API should not contain the core verification rules.

---

## Verification Service

The verification service contains the business logic.

Conceptually:

```python
result = verification_service.verify(transaction)
```

It should determine whether a transaction is:

* valid
* verified
* duplicated
* failed

The verification service should remain independent of FastAPI so that other interfaces can use it later.

---

## Database

PostgreSQL stores transaction records and provides persistent state for the verification engine.

The database is responsible for enforcing important invariants such as transaction uniqueness.

The application uses SQLModel/SQLAlchemy to communicate with PostgreSQL.

---

## Repository

The repository layer separates database operations from business logic.

Examples of operations include:

```text
create_transaction()
get_transaction_by_reference()
transaction_exists()
```

This prevents the verification service from becoming tightly coupled to SQL queries and database implementation details.

---

# Transaction Model

A transaction contains information such as:

```text
ID
Bank
Transaction Date
Sender
Receiver
Amount
Transaction Reference
Transaction Type
Interface Timestamp
```

Financial amounts should be represented using `Decimal` rather than floating-point values.

Transaction references are treated as identifiers rather than mathematical numbers.

---

# Database Verification

A simplified verification process looks like:

```text
Incoming transaction
        │
        ▼
Validate fields
        │
        ▼
Find transaction reference
        │
        ▼
Does it already exist?
       / \
     Yes  No
      │    │
      ▼    ▼
 Duplicate  Continue verification
               │
               ▼
        Store transaction
               │
               ▼
            Verified
```

Database constraints are used alongside application logic so that correctness does not depend entirely on the API code.

---

# Testing Strategy

Testing is an important part of V1 because the verification engine must behave predictably for different transaction states.

### Unit tests

Test individual pieces of logic:

```text
Valid transaction
Invalid amount
Invalid transaction reference
Duplicate detection
Verification status
Schema validation
```

### Integration tests

Test interactions between components:

```text
FastAPI → Verification Service → PostgreSQL
```

The goal is to verify that the complete workflow works correctly, not just that individual functions work in isolation.

---

# Development Strategy

V1 is intentionally being developed incrementally.

### Phase 1 — Database Foundation

* [ ] Finalize transaction model
* [ ] Configure PostgreSQL
* [ ] Configure database sessions
* [ ] Implement repository
* [ ] Implement transaction creation
* [ ] Implement transaction lookup
* [ ] Add database constraints/indexes

### Phase 2 — Verification Engine

* [ ] Define `VerificationResult`
* [ ] Implement validation rules
* [ ] Implement verification service
* [ ] Implement duplicate detection
* [ ] Connect verification service to repository
* [ ] Return standardized results

### Phase 3 — API

* [ ] Implement verification endpoint
* [ ] Connect endpoint to verification service
* [ ] Implement proper HTTP responses
* [ ] Implement API-level error handling

### Phase 4 — Testing

* [ ] Unit tests
* [ ] Database integration tests
* [ ] API tests
* [ ] Edge-case testing
* [ ] Duplicate/race-condition testing

### V1 Completion Criteria

V1 is considered complete when the system can reliably:

```text
Receive structured transaction data
            ↓
Validate it
            ↓
Check PostgreSQL
            ↓
Detect duplicates
            ↓
Determine verification status
            ↓
Return a standardized result
```

---

# Future Development

V1 provides the core engine that future components will use.

## V2 — OCR & File Processing

Future versions will allow users to submit:

* Images
* PDFs
* Screenshots of receipts

The future pipeline will look like:

```text
Receipt Image/PDF
       ↓
File Processing
       ↓
OCR
       ↓
Receipt Parser
       ↓
Structured Transaction
       ↓
V1 Verification Engine
       ↓
VerificationResult
```

The important design goal is that OCR should **produce structured transaction data** rather than implementing verification itself.

---

# V3 — Telegram Interface

A Telegram bot can later act as another interface:

```text
Telegram
    ↓
Telegram Adapter
    ↓
Verification Engine
    ↓
VerificationResult
    ↓
Telegram Response
```

The verification engine should not need to know that the request originated from Telegram.

---

# Future External Verification

External bank or payment-system APIs can eventually be added through provider interfaces.

Conceptually:

```text
             Verification Service
                      │
                      ▼
             Verification Provider
                /           \
               /             \
              ▼               ▼
       Mock Provider      Bank Provider
```

This allows external integrations to be added without rewriting the core verification engine.

---

# Design Principles

The project follows several important principles:

### Separation of concerns

The API, database, and verification logic should have clearly defined responsibilities.

### Modularity

New interfaces and verification providers should be addable without rewriting the core engine.

### Database integrity

Important invariants should be enforced by PostgreSQL as well as application logic.

### Explicit results

Verification should return a standardized result rather than arbitrary responses.

### Testability

Core business logic should be testable independently of FastAPI and external interfaces.

### Incremental development

The project is developed from a working core toward more complex functionality rather than implementing every feature simultaneously.

---

# Technology Stack

| Component              | Technology                     |
| ---------------------- | ------------------------------ |
| Language               | Python                         |
| API                    | FastAPI                        |
| Validation             | Pydantic                       |
| ORM / Database Layer   | SQLModel / SQLAlchemy          |
| Database               | PostgreSQL                     |
| Testing                | Pytest                         |
| Future OCR             | Tesseract                      |
| Future Interface       | Telegram                       |
| Future File Processing | PDF/Image processing libraries |

---

# Current Status

**Version:** `V1 — In Development`

The current implementation contains the initial FastAPI and database foundation.

The remaining core work is primarily:

* Database repository
* Verification service
* Verification result
* Duplicate detection
* Error handling
* Tests

Once these components are complete, the V1 core verification engine will be considered finished.

---

# Long-Term Vision

The long-term goal is not simply to build a receipt API.

The goal is to build a **modular transaction verification engine** that can accept transaction information from multiple sources while keeping the underlying verification logic independent.

```text
                     ┌──────────────┐
                     │    Telegram  │
                     └──────┬───────┘
                            │
                     ┌──────▼───────┐
                     │     OCR      │
                     └──────┬───────┘
                            │
                     ┌──────▼───────┐
                     │ Receipt      │
                     │ Parser       │
                     └──────┬───────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  Verification Engine │
                 └──────────┬───────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       ┌──────────────┐           ┌──────────────┐
       │  PostgreSQL  │           │ External APIs│
       └──────────────┘           └──────────────┘
```

**V1 builds the center of this system.**

Everything else can be added around it later.
