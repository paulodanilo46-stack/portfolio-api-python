from fastapi import APIRouter, HTTPException

from dtos.profileDto import ProfileDto
from dtos.profileResponseDto import ProfileResponseDto
from repositories import profileRepository


router = APIRouter(
    prefix="/api/profiles",
    tags=["Profiles"]
)


@router.post("", response_model=ProfileResponseDto)
def criar_profile(profile: ProfileDto):

    resultado = profileRepository.criar(
        profile.nome,
        profile.email,
        profile.bio
    )

    return ProfileResponseDto(
        id=resultado[0],
        nome=resultado[1],
        email=resultado[2],
        bio=resultado[3]
    )


@router.get("/{id}", response_model=ProfileResponseDto)
def buscar_profile(id: int):

    resultado = profileRepository.buscar_por_id(id)

    if resultado is None:
        raise HTTPException(
            status_code=404,
            detail="Profile não encontrado."
        )

    return ProfileResponseDto(
        id=resultado[0],
        nome=resultado[1],
        email=resultado[2],
        bio=resultado[3]
    )