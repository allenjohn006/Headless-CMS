from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.db.models import Collection, Field
from app.schemas.dynamic import CollectionCreate, Collection as CollectionSchema, FieldCreate, Field as FieldSchema
from app.api.dependencies import get_current_active_admin

router = APIRouter()

@router.post("/", response_model=CollectionSchema)
def create_collection(
    collection_in: CollectionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    """
    Create a new Collection (Admin only)
    """
    collection = db.query(Collection).filter(Collection.slug == collection_in.slug).first()
    if collection:
        raise HTTPException(status_code=400, detail="Collection slug already exists")
    
    new_collection = Collection(
        name=collection_in.name,
        slug=collection_in.slug,
        description=collection_in.description
    )
    db.add(new_collection)
    db.commit()
    db.refresh(new_collection)
    return new_collection

@router.get("/", response_model=List[CollectionSchema])
def get_collections(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all Collections
    """
    collections = db.query(Collection).offset(skip).limit(limit).all()
    return collections

@router.post("/{collection_id}/fields", response_model=FieldSchema)
def create_field(
    collection_id: UUID,
    field_in: FieldCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_admin)
):
    """
    Add a Field to a Collection (Admin only)
    """
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
        
    field = db.query(Field).filter(Field.collection_id == collection_id, Field.name == field_in.name).first()
    if field:
        raise HTTPException(status_code=400, detail="Field name already exists in this collection")

    new_field = Field(
        collection_id=collection_id,
        name=field_in.name,
        field_type=field_in.field_type,
        is_required=field_in.is_required,
        validations=field_in.validations
    )
    db.add(new_field)
    db.commit()
    db.refresh(new_field)
    return new_field

@router.get("/{collection_id}/fields", response_model=List[FieldSchema])
def get_fields(
    collection_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get all Fields for a Collection
    """
    fields = db.query(Field).filter(Field.collection_id == collection_id).all()
    return fields
