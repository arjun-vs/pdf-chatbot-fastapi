import os
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, File, UploadFile, Form, HTTPException, status
from fastapi.responses import StreamingResponse
load_dotenv()
from .database import engine, Base
from . import models
from . import schemas, auth
from fastapi import Depends
from sqlalchemy.orm import Session
from .token_blacklist import blacklist_token
from .utils import extract_text_from_pdf
from .llm import ask_llm, stream_llm
from .cache import get_from_cache, save_to_cache

app = FastAPI(title="PDF Chatbot")

Base.metadata.create_all(bind=engine)


@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    return auth.signup(user, db)

@app.post("/login")
def login(user:schemas.UserLogin, db: Session = Depends(auth.get_db)):
    return auth.login(user, db)

@app.post("/logout")
def logout(token: str = Depends(auth.oauth2_scheme)):
    blacklist_token(token)
    return {"message": "Successfully logged out."}

@app.post("/chat", response_model=schemas.ChatResponse)
async def chat(file: UploadFile = File(...), question: str = Form(...), current_user: models.User = Depends(auth.get_current_user), stream: bool = Form(False)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Please upload a PDF file.")
    
    file_bytes = file.file.read()
    pdf_text = extract_text_from_pdf(file_bytes)
    
    if not pdf_text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to extract text from the PDF file.")
    
    if stream:
        return StreamingResponse(stream_llm(pdf_text, question), media_type="text/event-stream")
    
    cache_key = f"{pdf_text}-{question}"

    cached_answer = get_from_cache(cache_key)
    if cached_answer:
        return {"user": current_user.email, "question": question, "answer": cached_answer}
    
    try:
        answer = await ask_llm(pdf_text, question)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"LLM service error: {str(e)}")
    save_to_cache(cache_key, answer)
    
    return {"user": current_user.email, "question": question, "answer": answer}

@app.get("/llm-models")
def get_llm_models(current_user: models.User = Depends(auth.get_current_user)):
    api_key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = httpx.get(url, headers=headers)
    return {"requested_user": current_user.email, "models": response.json()}
