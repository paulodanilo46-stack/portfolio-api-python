from pydantic import BaseModel


class ProjectDto(BaseModel):
    nome: str
    profile_id: int
    tecnologia_ids: list[int]