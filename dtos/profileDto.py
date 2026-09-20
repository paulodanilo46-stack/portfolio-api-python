from pydantic import BaseModel, EmailStr


class ProfileDto(BaseModel):
    nome: str
    email: EmailStr
    bio: str | None = None