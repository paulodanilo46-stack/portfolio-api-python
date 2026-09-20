from pydantic import BaseModel


class ProfileResponseDto(BaseModel):
    id: int
    nome: str
    email: str
    bio: str | None = None