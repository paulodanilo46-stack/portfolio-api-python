from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_connection

from dtos.projectDto import ProjectDto
from dtos.projectResponseDto import ProjectResponseDto
from repositories import projectRepository

class Feedback(BaseModel):
    nota: int
    comentario: str

router = APIRouter(
    prefix="/api/projects",
    tags=["Projetos"]
)

@router.get("", response_model=list[ProjectResponseDto])
def listar_projetos(
    tecnologia: str | None = None,
    pagina: int = 1,
    limite: int = 10
):
    if pagina < 1:
        pagina = 1

    if limite < 1:
        limite = 10

    resultados = projectRepository.listar(
        tecnologia,
        pagina,
        limite
    )

    return [
        ProjectResponseDto(
            id=projeto[0],
            nome=projeto[1],
            profile_id=projeto[2],
            media_avaliacao=float(projeto[3]),
            upvotes=projeto[4],
            tecnologia_ids=projeto[5]
        )
        for projeto in resultados
    ]

@router.post("", response_model=ProjectResponseDto)
def criar_projeto(project: ProjectDto):

    resultado = projectRepository.criar(
        project.nome,
        project.profile_id,
        project.tecnologia_ids
    )

    return ProjectResponseDto(
        id=resultado[0],
        nome=resultado[1],
        profile_id=resultado[2],
        media_avaliacao=float(resultado[3]),
        upvotes=resultado[4],
        tecnologia_ids=project.tecnologia_ids
    )
@router.post("/{id}/feedbacks")
def adicionar_feedback(id: int, feedback: Feedback):
    if feedback.nota < 1 or feedback.nota > 5:
        raise HTTPException(
            status_code=400,
            detail="A nota deve estar entre 1 e 5."
        )

    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id FROM projects WHERE id = %s",
        (id,)
    )

    projeto = cursor.fetchone()

    if projeto is None:
        cursor.close()
        conexao.close()

        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado."
        )

    cursor.execute("""
        INSERT INTO feedbacks (projeto_id, nota, comentario)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (
        id,
        feedback.nota,
        feedback.comentario
    ))

    feedback_id = cursor.fetchone()[0]

    cursor.execute("""
        SELECT AVG(nota)
        FROM feedbacks
        WHERE projeto_id = %s
    """, (id,))

    media = cursor.fetchone()[0]

    cursor.execute("""
        UPDATE projects
        SET media_avaliacao = %s
        WHERE id = %s
    """, (media, id))

    conexao.commit()

    cursor.close()
    conexao.close()

    return {
        "mensagem": "Feedback registrado com sucesso.",
        "feedback_id": feedback_id,
        "projeto_id": id,
        "nota": feedback.nota,
        "comentario": feedback.comentario,
        "media_avaliacao": float(media)
    }
    
@router.put("/{id}/upvote")
def dar_upvote(id: int):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE projects
        SET upvotes = upvotes + 1
        WHERE id = %s
        RETURNING id, nome, profile_id, media_avaliacao, upvotes
    """, (id,))

    projeto = cursor.fetchone()

    if projeto is None:
        cursor.close()
        conexao.close()

        raise HTTPException(
            status_code=404,
            detail="Projeto não encontrado."
        )

    conexao.commit()

    cursor.close()
    conexao.close()

    return {
        "mensagem": "Upvote registrado com sucesso.",
        "id": projeto[0],
        "nome": projeto[1],
        "profile_id": projeto[2],
        "media_avaliacao": float(projeto[3]),
        "upvotes": projeto[4]
    }