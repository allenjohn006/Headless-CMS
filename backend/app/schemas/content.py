from pydantic import BaseModel
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import datetime

class ContentBase(BaseModel):
    data: Dict[str, Any]
    status: str = "Draft"

class ContentCreate(ContentBase):
    pass

class ContentUpdate(ContentBase):
    pass

class Content(ContentBase):
    id: UUID
    collection_id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
