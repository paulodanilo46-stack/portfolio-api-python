from pydantic import BaseModel


class TechnologyDto(BaseModel):
    nome: str