# PDF Chatbot App

FastAPI backend for user authentication and PDF-based Q&A using Groq's chat completions.

## Features
- User signup/login with JWT authentication
- PDF upload and text extraction
- Ask questions against extracted PDF text
- Optional streaming responses (Server-Sent Events)

## Requirements
- Python 3.12+
- SQLite (default, uses `database.db` in project root)

## Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate      # Windows (PowerShell)
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root. Example:
   ```env
   # .env example
   DATABASE_URL=sqlite+aiosqlite:///./database.db
   SECRET_KEY=your_jwt_secret_here
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=groq-model-name
   ```

## Run
Start the development server:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## API Endpoints
- `POST /signup` — create a user
- `POST /login` — obtain access token (JWT)
- `POST /logout` — invalidate current token
- `POST /chat` — upload a PDF and ask a question
- `GET /llm-models` — list available Groq models

### `/chat` example (curl)
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@/path/to/file.pdf" \
  -F "question=What is this document about?"
```

### `/chat` streaming example (Server-Sent Events)
Set `stream=true` to receive streaming responses:
```bash
curl -N -X POST "http://127.0.0.1:8000/chat" \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@/path/to/file.pdf" \
  -F "question=Summarize this file" \
  -F "stream=true"
```

## Notes
- By default the app uses SQLite and stores the file `database.db` in the project root.
- Ensure `GROQ_API_KEY` (and any other required keys) are set in `.env` before starting the server.
- For production, replace SQLite with a production-ready database and secure the `SECRET_KEY`.
