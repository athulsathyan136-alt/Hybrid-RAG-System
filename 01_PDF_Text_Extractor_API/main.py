from fastapi import FastAPI, UploadFile, File, HTTPException
from pypdf import PdfReader
import io

app = FastAPI(
    title="PDF Text Extractor API",
    description="Upload a PDF and extract its text",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "PDF Text Extractor API is running"
    }


@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    contents = await file.read()

    try:
        pdf_file = io.BytesIO(contents)
        reader = PdfReader(pdf_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return {
            "filename": file.filename,
            "pages": len(reader.pages),
            "characters": len(text),
            "preview": text[:2000]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Could not process PDF: {str(error)}"
        )