import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from embedding_service import (
    extract_text_from_pdf,
    generate_embeddings,
    save_embeddings_to_faiss,
    query_embeddings,
    load_context_from_indices,
)

app = FastAPI()

@app.post("/upload", summary="Upload a document and generate embeddings")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document, extract its text, generate embeddings, and save them.
    """
    file_path = f"workspace/{file.filename}"
    try:
        # Save the uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Extract text and generate embeddings
        text = extract_text_from_pdf(file_path)
        if not text:
            raise HTTPException(status_code=400, detail="No text found in the uploaded document.")
        
        embedding = generate_embeddings(text)
        save_embeddings_to_faiss(embedding, text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    return {"message": "Document uploaded and embeddings generated successfully."}

@app.post("/ask", summary="Ask a question using the uploaded document")
def ask_question(query: str):
    """
    Query the embeddings and retrieve relevant context for the given question.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        indices = query_embeddings(query)
        context = load_context_from_indices(indices)
        return {"context": context, "query": query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/")
def root():
    """
    Root endpoint for the AI microservice.
    """
    return {"message": "Welcome to the AI Microservice"}