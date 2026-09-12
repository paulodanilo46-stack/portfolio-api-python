from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException


from routes.projects import router as projects_router

app = FastAPI(
    title="Portfolio API",
    description="API para gerenciamento do projeto de portfólio",
    version="1.0.0"
)

app.include_router(projects_router)


@app.exception_handler(HTTPException)
async def tratar_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": exc.detail
        }
    )


@app.exception_handler(RequestValidationError)
async def tratar_erro_validacao(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "erro": "Dados inválidos.",
            "detalhes": exc.errors()
        }
    )

@app.get("/")
def inicio():
    return {
        "mensagem": "API funcionando!"
    }