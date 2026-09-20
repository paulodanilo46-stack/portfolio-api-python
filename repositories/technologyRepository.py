from database import get_connection


def criar(nome):
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO technologies (nome)
        VALUES (%s)
        RETURNING id, nome
    """, (nome,))

    technology = cursor.fetchone()

    conexao.commit()

    cursor.close()
    conexao.close()

    return technology


def listar():
    conexao = get_connection()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome
        FROM technologies
        ORDER BY id
    """)

    technologies = cursor.fetchall()

    cursor.close()
    conexao.close()

    return technologies