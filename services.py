from sqlalchemy.orm import Session
from app.models import Contact, LinkPrecedence
from sqlalchemy import or_

def identify_contact(db: Session, email: str = None, phoneNumber: str = None):

    # 1️⃣ Find all contacts matching email or phone
    existing_contacts = db.query(Contact).filter(
        or_(
            Contact.email == email,
            Contact.phoneNumber == phoneNumber
        )
    ).all()

    if not existing_contacts:
        # 2️⃣ No match → create primary
        new_contact = Contact(
            email=email,
            phoneNumber=phoneNumber,
            linkPrecedence=LinkPrecedence.primary
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        return build_response([new_contact], new_contact)

    # 3️⃣ Find all linked contacts recursively
    all_related = set(existing_contacts)

    for contact in existing_contacts:
        if contact.linkedId:
            primary = db.query(Contact).filter(Contact.id == contact.linkedId).first()
            if primary:
                all_related.add(primary)

    all_related = list(all_related)

    # 4️⃣ Find oldest primary
    primary_contact = min(
        [c for c in all_related if c.linkPrecedence == LinkPrecedence.primary],
        key=lambda x: x.createdAt
    )

    # 5️⃣ Convert other primaries to secondary if needed
    for contact in all_related:
        if contact.id != primary_contact.id and contact.linkPrecedence == LinkPrecedence.primary:
            contact.linkPrecedence = LinkPrecedence.secondary
            contact.linkedId = primary_contact.id

    # 6️⃣ If new info → create secondary
    emails = [c.email for c in all_related if c.email]
    phones = [c.phoneNumber for c in all_related if c.phoneNumber]

    if (email and email not in emails) or (phoneNumber and phoneNumber not in phones):
        new_secondary = Contact(
            email=email,
            phoneNumber=phoneNumber,
            linkPrecedence=LinkPrecedence.secondary,
            linkedId=primary_contact.id
        )
        db.add(new_secondary)
        db.commit()
        db.refresh(new_secondary)
        all_related.append(new_secondary)

    db.commit()

    return build_response(all_related, primary_contact)

def build_response(all_contacts, primary_contact):

    emails = []
    phones = []
    secondary_ids = []

    for c in sorted(all_contacts, key=lambda x: x.createdAt):
        if c.email and c.email not in emails:
            emails.append(c.email)
        if c.phoneNumber and c.phoneNumber not in phones:
            phones.append(c.phoneNumber)
        if c.linkPrecedence == LinkPrecedence.secondary:
            secondary_ids.append(c.id)

    return {
        "contact": {
            "primaryContatctId": primary_contact.id,
            "emails": emails,
            "phoneNumbers": phones,
            "secondaryContactIds": secondary_ids
        }
    }    