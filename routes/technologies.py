from fastapi import APIRouter, HTTPException

from dtos.technologyDto import TechnologyDto
from dtos.technologyResponseDto import TechnologyResponseDto
from repositories import technologyRepository


router = APIRouter(
    prefix="/api/technologies",
    tags=["Technologies"]
)


@router.post("", response_model=TechnologyResponseDto)
def criar_technology(technology: TechnologyDto):

    try:
        resultado = technologyRepository.criar(
            technology.nome
        )

        return TechnologyResponseDto(
            id=resultado[0],
            nome=resultado[1]
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível cadastrar a tecnologia."
        )


@router.get("", response_model=list[TechnologyResponseDto])
def listar_technologies():

    resultados = technologyRepository.listar()

    return [
        TechnologyResponseDto(
            id=technology[0],
            nome=technology[1]
        )
        for technology in resultados
    ]