from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import uuid
from typing import Dict, Any

from app.db.session import get_db
from app.db.models import Media
from app.api.dependencies import get_current_active_editor
from app.services.optimization import optimize_image
from app.core.config import settings

router = APIRouter()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_editor)
):
    """
    Upload an image, optimize it, and generate WebP variants.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")
        
    file_bytes = await file.read()
    
    # Generate unique filename for WebP
    base_name = str(uuid.uuid4())
    optimized_filename = f"{base_name}.webp"
    optimized_filepath = os.path.join(settings.UPLOAD_DIR, optimized_filename)
    
    # Optimize and save
    success = optimize_image(file_bytes, optimized_filepath, max_width=1200)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to optimize image")
        
    # Get final size
    size_bytes = os.path.getsize(optimized_filepath)
    url = f"/static/uploads/{optimized_filename}"
    
    # Save metadata to DB
    media = Media(
        filename=optimized_filename,
        url=url,
        mime_type="image/webp",
        size_bytes=size_bytes,
        uploaded_by=current_user.id
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    
    return {
        "id": media.id,
        "url": media.url,
        "filename": media.filename,
        "mime_type": media.mime_type
    }

@router.delete("/{media_id}", status_code=204)
def delete_media(
    media_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_editor)
):
    """
    Delete a media asset and its file (Editors/Admins only)
    """
    media = db.query(Media).filter(Media.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    filepath = os.path.join(settings.UPLOAD_DIR, media.filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    db.delete(media)
    db.commit()
    return None
