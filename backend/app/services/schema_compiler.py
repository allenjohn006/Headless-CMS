from typing import Tuple, List, Dict, Any
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.models import Field

def validate_content_schema(db: Session, collection_id: UUID, payload: Dict[str, Any]) -> Tuple[bool, List[Dict[str, str]]]:
    """
    Validates JSON data against the dynamically defined fields for a collection.
    Returns (is_valid, errors_list)
    """
    fields = db.query(Field).filter(Field.collection_id == collection_id).all()
    errors = []
    
    for field in fields:
        value = payload.get(field.name)
        
        if field.is_required and value is None:
            errors.append({"field": field.name, "message": "This field is required."})
            continue
            
        if value is not None:
            # Type Checking
            if field.field_type == "Text" and not isinstance(value, str):
                errors.append({"field": field.name, "message": "Must be a string."})
            elif field.field_type == "Number" and not isinstance(value, (int, float)):
                errors.append({"field": field.name, "message": "Must be a number."})
            elif field.field_type == "Boolean" and not isinstance(value, bool):
                errors.append({"field": field.name, "message": "Must be a boolean."})
                
            # Validation logic based on field.validations JSON
            if isinstance(value, str):
                min_len = field.validations.get("min_length")
                if min_len is not None and len(value) < min_len:
                    errors.append({"field": field.name, "message": f"Minimum length is {min_len}."})
                    
                max_len = field.validations.get("max_length")
                if max_len is not None and len(value) > max_len:
                    errors.append({"field": field.name, "message": f"Maximum length is {max_len}."})
                    
    # Also check if payload has extra fields not in schema
    allowed_keys = {f.name for f in fields}
    for key in payload.keys():
        if key not in allowed_keys:
            errors.append({"field": key, "message": "Field is not defined in the schema."})

    return len(errors) == 0, errors
