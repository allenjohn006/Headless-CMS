import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, BigInteger, JSON, CHAR
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import relationship
from app.db.session import Base

class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise String(36).
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            from sqlalchemy.dialects.postgresql import UUID as pgUUID
            return dialect.type_descriptor(pgUUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            return value

class User(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False) # 'Admin' or 'Editor'
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

class Collection(Base):
    __tablename__ = "collections"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    fields = relationship("Field", back_populates="collection", cascade="all, delete-orphan")
    contents = relationship("Content", back_populates="collection", cascade="all, delete-orphan")

class Field(Base):
    __tablename__ = "fields"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    collection_id = Column(GUID(), ForeignKey("collections.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    field_type = Column(String(50), nullable=False) # Text, Rich Text, Image, Number, etc.
    is_required = Column(Boolean, default=False)
    validations = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    collection = relationship("Collection", back_populates="fields")

class Content(Base):
    __tablename__ = "contents"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    collection_id = Column(GUID(), ForeignKey("collections.id", ondelete="CASCADE"))
    data = Column(JSON, nullable=False)
    status = Column(String(50), nullable=False) # 'Draft' or 'Published'
    created_by = Column(GUID(), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    collection = relationship("Collection", back_populates="contents")
    creator = relationship("User")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    content_id = Column(GUID(), ForeignKey("contents.id", ondelete="CASCADE"))
    previous_data = Column(JSON, nullable=False)
    changed_by = Column(GUID(), ForeignKey("users.id"))
    changed_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    content = relationship("Content")
    changer = relationship("User")

class Media(Base):
    __tablename__ = "media"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    mime_type = Column(String(100))
    size_bytes = Column(BigInteger)
    uploaded_by = Column(GUID(), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    uploader = relationship("User")
