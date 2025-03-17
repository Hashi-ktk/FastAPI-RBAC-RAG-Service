import os
import faiss
import openai
import numpy as np  # Import numpy
from PyPDF2 import PdfReader

openai.api_key = os.getenv("OPENAI_API_KEY")

EMBEDDINGS_FILE = "workspace/embeddings.index"
CONTEXT_FILE = "workspace/context.txt"

def extract_text_from_pdf(pdf_file_path: str) -> str:
    """Extract text from a PDF file with improved error checking."""
    try:
        reader = PdfReader(pdf_file_path)
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return ""

    text = ""
    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()
        if page_text:
            text += page_text
        else:
            print(f"No text extracted from page {page_number}.")
            
    if text:
        print("Extracted text:\n", text)
    else:
        print("No extractable text found in the PDF.")

    return text

def generate_embeddings(text: str) -> list:
    """Generate embeddings for the given text using OpenAI."""
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    print(response.data[0].embedding)
    return response.data[0].embedding

def save_embeddings_to_faiss(embedding: list, context: str):
    """Save the embedding and context to a FAISS index."""
    dimension = len(embedding)
    print(dimension)
    index = faiss.IndexFlatL2(dimension)
    print(index)

    # Convert the embedding list to a numpy array
    embedding_array = np.array([embedding], dtype='float32')

    if os.path.exists(EMBEDDINGS_FILE):
        index = faiss.read_index(EMBEDDINGS_FILE)
    else:
        index = faiss.IndexFlatL2(dimension)
    
    # Add the embedding to the index
    index.add(embedding_array)
    faiss.write_index(index, EMBEDDINGS_FILE)

    # Save the context to a file (overwrite previous context)
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        f.write(context)

def load_embeddings_from_faiss() -> faiss.IndexFlatL2:
    """Load the FAISS index."""
    if not os.path.exists(EMBEDDINGS_FILE):
        raise FileNotFoundError("No embeddings found. Please upload a document first.")
    return faiss.read_index(EMBEDDINGS_FILE)

def query_embeddings(query: str) -> list:
    """Query the FAISS index and return the indices of the closest matches."""
    index = load_embeddings_from_faiss()
    query_embedding = generate_embeddings(query)
    
    # Convert the query embedding list to a numpy array
    query_embedding_array = np.array([query_embedding], dtype='float32')
    
    _, indices = index.search(query_embedding_array, k=1)
    return indices[0]

def load_context_from_indices(indices: list) -> str:
    """Load the context corresponding to the given indices."""
    if not os.path.exists(CONTEXT_FILE):
        raise FileNotFoundError("No context found. Please upload a document first.")
    with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
        context = f.read()
    return context