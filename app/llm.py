import os
import httpx
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = os.getenv("GROQ_URL")
GROQ_MODEL = os.getenv("GROQ_MODEL")

async def ask_llm(pdf_text: str, question: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    question = question.strip()
    prompt = f""" 
    You are a helpful assistant. Answer the question strictly based on the PDF content below
    PDF content: {pdf_text}
    Question: {question} 
    """
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(GROQ_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    
    return data["choices"][0]["message"]["content"]

async def stream_llm(pdf_text: str, question: str):
    question = question.strip()

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    prompt = f""" 
    You are a helpful assistant. Answer the question strictly based on the PDF content below
    PDF content: {pdf_text}
    Question: {question} 
    """

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "stream": True
    }

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST", GROQ_URL, headers=headers, json=payload
        ) as response:

            async for line in response.aiter_lines():
                if not line or not line.startswith("data:"):
                    continue

                data = line.replace("data:", "").strip()
                if data == "[DONE]":
                    break

                chunk = json.loads(data)
                delta = chunk["choices"][0]["delta"].get("content")
                if delta:
                    yield delta