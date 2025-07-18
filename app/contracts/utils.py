from docx import Document
import PyPDF2
from fastapi import UploadFile, HTTPException, status
from io import BytesIO
import json
from google import genai

from .prompt import CONTRACT_EXTRACTION_PROMPT
from ..config import settings

try:
    gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    GEMINI_MODEL_NAME = "gemini-2.5-flash"
except Exception as e:
    print(f"Erro ao inicializar o cliente Gemini: {e}. Verifique sua GEMINI_API_KEY no .env")
    gemini_client = None

def extract_text_from_pdf(file: UploadFile) -> str:
    pdf_reader = PyPDF2.PdfReader(BytesIO(file.file.read()))
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(file: UploadFile) -> str:
    document = Document(BytesIO(file.file.read()))
    return "\n".join([paragraph.text for paragraph in document.paragraphs])

def __parse_and_normalize_json(ai_output: str) -> dict:
    text = ai_output.strip()

    # Remove markdown code block fences if present (```json ... ```)
    if text.startswith("```json") and text.endswith("```"):
        text = text[7:-3].strip()
    elif text.startswith("```") and text.endswith("```"):
        text = text[3:-3].strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI returned a wrong JSON {e}"
        )

    return parsed

async def process_contract_with_ai(contract_text: str) -> dict:
    if not gemini_client or not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API Key for Gemini service not configured or client initialization failed."
        )

    prompt = CONTRACT_EXTRACTION_PROMPT.format(contract_text=contract_text)

    try:
        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=[prompt]
        )

        return __parse_and_normalize_json(response.text)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing contract with AI: {e} Please try again later or check API limits."
        )