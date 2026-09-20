from pydantic import BaseModel


class TechnologyResponseDto(BaseModel):
    id: int
    nome: str