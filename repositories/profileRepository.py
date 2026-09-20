from database import get_connection


def criar(nome, email, bio):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO profiles
        (nome, email, bio)
        VALUES (%s, %s, %s)
        RETURNING id, nome, email, bio
    """, (
        nome,
        email,
        bio
    ))

    profile = cursor.fetchone()

    conexao.commit()

    cursor.close()
    conexao.close()

    return profile


def buscar_por_id(id):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, email, bio
        FROM profiles
        WHERE id = %s
    """, (id,))

    profile = cursor.fetchone()

    cursor.close()
    conexao.close()

    return profile