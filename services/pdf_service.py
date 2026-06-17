from io import BytesIO
import PyPDF2


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes. Raises ValueError on failure."""
    if not file_bytes:
        raise ValueError("Empty file provided")

    try:
        reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        pages = []
        for p in range(len(reader.pages)):
            page = reader.pages[p]
            text = page.extract_text() or ""
            pages.append(text)
        return "\n".join(pages).strip()
    except Exception as e:
        raise ValueError(f"Failed to extract PDF text: {e}")
