from fastapi import FastAPI
from contextlib import asynccontextmanager
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)