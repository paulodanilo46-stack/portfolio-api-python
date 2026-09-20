from database import get_connection


def criar(nome, profile_id, tecnologia_ids):
    conexao = get_connection()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO projects
            (nome, profile_id)
            VALUES (%s, %s)
            RETURNING id, nome, profile_id, media_avaliacao, upvotes
        """, (
            nome,
            profile_id
        ))

        projeto = cursor.fetchone()
        projeto_id = projeto[0]

        for tecnologia_id in tecnologia_ids:
            cursor.execute("""
                INSERT INTO project_technologies
                (projeto_id, tecnologia_id)
                VALUES (%s, %s)
            """, (
                projeto_id,
                tecnologia_id
            ))

        conexao.commit()

        return projeto

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()


def listar(tecnologia=None, pagina=1, limite=10):
    conexao = get_connection()
    cursor = conexao.cursor()

    deslocamento = (pagina - 1) * limite

    if tecnologia:
        cursor.execute("""
            SELECT
                p.id,
                p.nome,
                p.profile_id,
                p.media_avaliacao,
                p.upvotes,
                ARRAY(
                    SELECT pt.tecnologia_id
                    FROM project_technologies pt
                    WHERE pt.projeto_id = p.id
                ) AS tecnologia_ids
            FROM projects p
            WHERE EXISTS (
                SELECT 1
                FROM project_technologies pt
                INNER JOIN technologies t
                    ON t.id = pt.tecnologia_id
                WHERE pt.projeto_id = p.id
                AND LOWER(t.nome) = LOWER(%s)
            )
            ORDER BY p.id
            LIMIT %s OFFSET %s
        """, (
            tecnologia,
            limite,
            deslocamento
        ))

    else:
        cursor.execute("""
            SELECT
                p.id,
                p.nome,
                p.profile_id,
                p.media_avaliacao,
                p.upvotes,
                ARRAY(
                    SELECT pt.tecnologia_id
                    FROM project_technologies pt
                    WHERE pt.projeto_id = p.id
                ) AS tecnologia_ids
            FROM projects p
            ORDER BY p.id
            LIMIT %s OFFSET %s
        """, (
            limite,
            deslocamento
        ))

    projetos = cursor.fetchall()

    cursor.close()
    conexao.close()

    return projetos