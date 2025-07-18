import os
from fastapi import FastAPI, HTTPException, Request, Depends
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from app import models
from app.auth.service import get_current_user
from .auth.router import router as auth_router
from .contracts.router import router as contracts_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ao iniciar a aplicação
    yield
    # Ao encerrar a aplicação (se necessário, fechar conexões, etc.)
    # Pass

app = FastAPI(
    title="Biofy Contracts API",
    description="API para upload e análise de contratos com IA",
    version="1.0.0",
    lifespan=lifespan
)

# Incluir os routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(contracts_router, prefix="/api/v1")

# Caminho para a pasta front-end
FRONT_END_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "front_end"))

# Montar diretório de images públicas
app.mount(
    "/images",
    StaticFiles(directory=os.path.join(FRONT_END_DIR, "images")),
    name="images",
)

@app.get("/{full_path:path}", response_class=FileResponse)
async def serve_frontend(
    full_path: str,
):
    """
    Serve os arquivos do front-end.

    A página `index.html` é pública. Todas as outras são protegidas por JWT.
    """
    # Se o caminho for vazio, serve o `index.html`
    if not full_path:
        full_path = "index.html"

    # Constrói o caminho do arquivo solicitado
    file_path = os.path.join(FRONT_END_DIR, full_path)

    # Verifica se o arquivo existe
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Página não encontrada")

    return FileResponse(file_path)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)