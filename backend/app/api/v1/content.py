from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Dict, List
from uuid import UUID

from app.db.session import get_db
from app.db.models import Collection, Content
from app.api.dependencies import get_current_active_editor
from app.services.schema_compiler import validate_content_schema
from app.services.versioning import create_audit_log
from app.schemas.content import ContentCreate, ContentUpdate, Content as ContentSchema

router = APIRouter()

@router.get("/{collection_slug}")
def get_collection_content(
    collection_slug: str,
    status: str = Query(None, description="Filter by Draft or Published"),
    sort: str = Query("-created_at"),
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Omnichannel API Gateway: Fetch content dynamically.
    Publicly accessible (or protected by API Key in the future).
    """
    collection = db.query(Collection).filter(Collection.slug == collection_slug).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
        
    query = db.query(Content).filter(Content.collection_id == collection.id)
    if status:
        query = query.filter(Content.status == status)
    
    if sort.startswith("-"):
        query = query.order_by(Content.created_at.desc())
    else:
        query = query.order_by(Content.created_at.asc())
        
    total = query.count()
    contents = query.offset(offset).limit(limit).all()
    
    return {
        "data": [
            {
                "id": c.id,
                "data": c.data,
                "status": c.status,
                "created_at": c.created_at,
                "updated_at": c.updated_at
            }
            for c in contents
        ],
        "meta": {"total": total, "limit": limit, "offset": offset}
    }

@router.post("/{collection_slug}", response_model=ContentSchema, status_code=201)
def create_collection_content(
    collection_slug: str,
    payload: ContentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_editor)
):
    """
    Dynamic Content Create (Editors/Admins only)
    """
    collection = db.query(Collection).filter(Collection.slug == collection_slug).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
        
    is_valid, errors = validate_content_schema(db, collection.id, payload.data)
    if not is_valid:
        raise HTTPException(status_code=400, detail={"errors": errors})
        
    new_content = Content(
        collection_id=collection.id,
        data=payload.data,
        status=payload.status,
        created_by=current_user.id
    )
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    
    return new_content

@router.put("/{collection_slug}/{content_id}", response_model=ContentSchema)
def update_collection_content(
    collection_slug: str,
    content_id: UUID,
    payload: ContentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_editor)
):
    """
    Dynamic Content Update with Audit Logging
    """
    collection = db.query(Collection).filter(Collection.slug == collection_slug).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
        
    content = db.query(Content).filter(Content.id == content_id, Content.collection_id == collection.id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
        
    is_valid, errors = validate_content_schema(db, collection.id, payload.data)
    if not is_valid:
        raise HTTPException(status_code=400, detail={"errors": errors})
        
    # Create Audit Log before updating
    create_audit_log(db, content, current_user.id)
    
    content.data = payload.data
    content.status = payload.status
    db.commit()
    db.refresh(content)
    
    return content
