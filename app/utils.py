from io import BytesIO
from pypdf import PdfReader

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes), strict=False)
    text = ""
    for page in reader.pages:
        page_text = ""
        try:
            page_text = page.extract_text() or ""
        except Exception:
            try:
                page_text = page.extract_text(extraction_mode="layout") or ""
            except Exception:
                page_text = ""
        if page_text:
            text += page_text + "\n"
    return text.strip()
