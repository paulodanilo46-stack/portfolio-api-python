from pydantic import BaseModel


class ProjectResponseDto(BaseModel):
    id: int
    nome: str
    profile_id: int | None = None
    media_avaliacao: float
    upvotes: int
    tecnologia_ids: list[int] = []