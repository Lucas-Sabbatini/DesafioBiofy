# app/contracts/utils.py
from docx import Document
import PyPDF2
from fastapi import UploadFile, HTTPException, status
from io import BytesIO
import json
from typing import List, Dict, Any, Optional

# Importar do novo pacote google.genai
from google import genai
from google.genai import types # Importa os tipos para configurações e partes do conteúdo

from ..config import settings # Suas configurações com a API_KEY

# Inicializa o cliente Gemini uma vez globalmente.
# O Client() pode receber a api_key diretamente, garantindo que pegue do settings
try:
    gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    # Define o modelo que você vai usar. Use o Client para acessar os modelos.
    # Você pode usar 'gemini-pro' ou 'gemini-2.5-flash' ou outro modelo disponível.
    GEMINI_MODEL_NAME = "gemini-2.5-flash" # Ou "gemini-pro"
except Exception as e:
    # Captura o erro se a chave não estiver configurada no início
    print(f"Erro ao inicializar o cliente Gemini: {e}. Verifique sua GEMINI_API_KEY no .env")
    gemini_client = None # Define como None para tratamento posterior

def extract_text_from_pdf(file: UploadFile) -> str:
    pdf_reader = PyPDF2.PdfReader(BytesIO(file.file.read()))
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(file: UploadFile) -> str:
    document = Document(BytesIO(file.file.read()))
    return "\n".join([paragraph.text for paragraph in document.paragraphs])

async def process_contract_with_ai(contract_text: str) -> dict:
    # Verifica se o cliente Gemini foi inicializado com sucesso
    if not gemini_client or not settings.GEMINI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API Key for Gemini service not configured or client initialization failed."
        )

    prompt_template = f"""
    Analise o seguinte texto de contrato e extraia as seguintes informações no formato JSON.
    Se uma informação não for encontrada ou não se aplicar, retorne um array vazio ([]) para listas, um objeto vazio ({{}}) para dicionários, ou `null` para strings e outros valores únicos.

    Estrutura do JSON esperada:
    {{
        "parties": [], // Lista de strings com os nomes das partes envolvidas
        "monetary_values": [], // Lista de strings com valores monetários encontrados (ex: "R$ 10.000,00", "mil dólares")
        "main_obligations": [], // Lista de strings com as obrigações principais de cada parte
        "additional_data": {{}}, // Dicionário com dados adicionais importantes (ex: "objeto": "locação de imóvel", "vigencia": "5 anos")
        "termination_clause": null // String com o texto da cláusula de rescisão, se existir, ou null
    }}

    Texto do Contrato:
    ---
    {{contract_content}}
    ---
    """
    # Limite o texto para evitar exceder o limite de tokens da API (ex: 8000 caracteres)
    # O limite de tokens do Gemini varia por modelo. É uma boa prática truncar ou usar técnicas de chunking.
    limited_contract_text = contract_text[:8000] # Garante que não exceda um limite razoável

    # Construir o prompt final
    final_prompt = prompt_template.format(contract_content=limited_contract_text)

    try:
        # A nova API usa uma estrutura de `contents` que é uma lista de `Part` ou strings.
        # Para um prompt simples de texto, basta a string.
        # A `generate_content` é um método assíncrono, então `await` é necessário.
        response = await gemini_client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            # system_instruction é bom para definir o "papel" do modelo, mas para extração,
            # o prompt principal já faz o trabalho.
            # config=types.GenerateContentConfig(
            #     system_instruction="You are an expert contract analyst tasked with extracting specific information."
            # ),
            contents=[final_prompt] # Envia o prompt como uma lista de conteúdo
        )

        ai_output = response.text

        # Tenta parsear o JSON. A IA pode não retornar JSON perfeito
        try:
            # Remove markdown code block fences if present (```json ... ```)
            if ai_output.strip().startswith("```json") and ai_output.strip().endswith("```"):
                ai_output = ai_output.strip()[7:-3].strip()
            elif ai_output.strip().startswith("```") and ai_output.strip().endswith("```"):
                ai_output = ai_output.strip()[3:-3].strip()

            parsed_data = json.loads(ai_output)

        except json.JSONDecodeError as e:
            print(f"Erro ao parsear JSON da IA: {e}")
            print(f"Saída da IA bruta: \n{ai_output}") # Imprime para depuração
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI returned malformed JSON or unexpected response. Please check logs."
            )

        # Validação básica e padronização dos campos esperados
        # Garante que todos os campos estejam presentes com um valor padrão se ausentes
        extracted_data = {
            "parties": parsed_data.get("parties", []),
            "monetary_values": parsed_data.get("monetary_values", []),
            "main_obligations": parsed_data.get("main_obligations", []),
            "additional_data": parsed_data.get("additional_data", {}),
            "termination_clause": parsed_data.get("termination_clause", None),
        }

        return extracted_data

    except Exception as e:
        print(f"Erro na interação com a API de IA: {e}")
        # Uma verificação para o caso de a chave API estar ausente durante a chamada (embora já verificado antes)
        if "API key not found" in str(e) or "authentication" in str(e).lower():
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Gemini API Key is invalid or not provided. Please check your .env file."
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing contract with AI. Please try again later or check API limits."
        )