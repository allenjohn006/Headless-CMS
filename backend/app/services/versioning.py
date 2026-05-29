from sqlalchemy.orm import Session
from uuid import UUID
from app.db.models import Content, AuditLog

def create_audit_log(db: Session, content: Content, user_id: UUID):
    """
    Creates a snapshot of the current content before it gets updated.
    """
    audit_log = AuditLog(
        content_id=content.id,
        previous_data=content.data,
        changed_by=user_id
    )
    db.add(audit_log)
    db.commit()
