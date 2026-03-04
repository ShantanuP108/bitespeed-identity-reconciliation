# Bitespeed Identity Reconciliation Service

This project implements a backend service that identifies and links customer contacts based on email and phone number.

The goal is to consolidate multiple purchases made with different contact information into a single identity.

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Python

## API Endpoint

POST /identify

Example request:

{
  "email": "doc@fluxkart.com",
  "phoneNumber": "123456"
}

Example response:

{
  "contact": {
    "primaryContatctId": 1,
    "emails": ["doc@fluxkart.com"],
    "phoneNumbers": ["123456"],
    "secondaryContactIds": []
  }
}

## How It Works

1. When a request comes in, the system checks if any contact exists with the same email or phone number.
2. If no contact exists, a new primary contact is created.
3. If a contact exists, the system links them together.
4. The oldest contact becomes the primary contact.
5. All other contacts become secondary contacts linked to the primary.

## Running the project locally

Clone the repository
git clone <repo-link>
cd bitespeed-identity-reconciliation


Create virtual environment


python -m venv venv
source venv/bin/activate


Install dependencies


pip install -r requirements.txt


Set database environment variable


export DATABASE_URL=<your-postgres-url>


Run the server


uvicorn app.main:app --reload


Swagger documentation will be available at


http://localhost:8000/docs


## Deployment

The service is deployed on Render.

Live endpoint:
