from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

class FieldBase(BaseModel):
    name: str
    field_type: str # Text, Number, Boolean, RichText, Image
    is_required: bool = False
    validations: Dict[str, Any] = {}

class FieldCreate(FieldBase):
    pass

class Field(FieldBase):
    id: UUID
    collection_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class CollectionBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

class CollectionCreate(CollectionBase):
    pass

class Collection(CollectionBase):
    id: UUID
    created_at: datetime
    fields: List[Field] = []

    class Config:
        from_attributes = True
