from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.users import models, schemas
from app.auth.dependencies import get_db, get_current_user
from app.services.embedding_service import query_embeddings, load_context_from_indices
import openai

router = APIRouter()

@router.get("/me", response_model=schemas.UserRead)
def read_current_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Retrieve the current user's data.
    """
    return current_user

@router.put("/me", response_model=schemas.UserRead)
def update_current_user(
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Update the current user's data.
    """
    db_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only the fields provided in the request
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/ask")
def ask_question(
    question: schemas.QuestionRequest,
    current_user: models.User = Depends(get_current_user),
):
    """
    Allow users to ask questions using the GPT-4 model with RAG.
    """
    try:
        # Retrieve indices and context from FAISS
        indices = query_embeddings(question.query)
        context = load_context_from_indices(indices)

        # Use the context to query GPT-4
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question.query}"}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))