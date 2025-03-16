import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.users import models, schemas
from app.auth.dependencies import get_db, get_current_user
from app.auth.utils import hash_password
from fastapi import UploadFile, File
from app.services.embedding_service import extract_text_from_pdf, generate_embeddings, save_embeddings_to_faiss

router = APIRouter()


@router.post("/", response_model=schemas.UserRead)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to create users")
    
    hashed_password = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False,
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed: users.email" in str(e):
            raise HTTPException(status_code=400, detail="Email already exists")
        elif "UNIQUE constraint failed: users.username" in str(e):
            raise HTTPException(status_code=400, detail="Username already exists")
        else:
            raise HTTPException(status_code=400, detail="Database integrity error")
    return db_user

@router.get("/{user_id}", response_model=schemas.UserRead)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user")
    return db_user

@router.put("/{user_id}", response_model=schemas.UserRead)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=schemas.UserRead)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete users")
    db.delete(db_user)
    db.commit()
    return db_user

@router.get("/", response_model=list[schemas.UserRead])
def list_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view all users")
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
):
    """
    Allow admins to upload a PDF, extract its text, generate embeddings, and save them.
    """

    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to upload documents")

    # Define where to temporarily save the uploaded file
    file_path = f"workspace/{file.filename}"
    
    try:
        # Asynchronously save the uploaded file to disk
        with open(file_path, "wb") as f:
            content = await file.read()  # Read file contents asynchronously
            f.write(content)

        # Call external functions for text extraction, embeddings, etc.
        text = extract_text_from_pdf(file_path)
        embedding = generate_embeddings(text)
        save_embeddings_to_faiss(embedding, text)

    except Exception as e:
        # Handle errors during processing
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
    finally:
        # Clean up: Remove the temporary file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

    return {"message": "PDF uploaded and embeddings saved successfully"}
