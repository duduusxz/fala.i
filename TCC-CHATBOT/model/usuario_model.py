import pymysql
from werkzeug.security import generate_password_hash

# Configurações da conexão
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "tcc_sql",
     "cursorclass": pymysql.cursors.DictCursor # Isso é CRUCIAL para retornar dicionários!
}

def get_db_connection():
    return pymysql.connect(**db_config)

def cadastrar(rm, email, senha_hash):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO usuarios (rm, email, senha) VALUES (%s, %s, %s)
            ''', (rm, email, senha_hash))
            conn.commit()
    finally:
        conn.close()

def buscar_usuario_por_rm_e_email(rm, email):
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('SELECT * FROM usuarios WHERE rm = %s AND email = %s', (rm, email))
            return cursor.fetchone()
    finally:
        conn.close()

def buscar_usuario_por_email(email):
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
            return cursor.fetchone()
    finally:
        conn.close()

def atualizar_senha(email, nova_senha):
    nova_senha_hash = generate_password_hash(nova_senha)
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('UPDATE usuarios SET senha = %s WHERE email = %s', (nova_senha, email))
            conn.commit()
    finally:
        conn.close()

def listar_todos_usuarios():
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('SELECT * FROM usuarios')
            return cursor.fetchall()
    finally:
        conn.close()

def obter_ranking():
    conn = get_db_connection()
    try:
            with conn.cursor() as cursor:
                cursor.execute('''
                SELECT nome, pontos FROM tb_ranking ORDER BY pontos DESC;

                ''')
                return cursor.fetchall()
    finally:
                conn.close()   

def buscar_podio():
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM tb_ranking ORDER BY pontos DESC LIMIT 3")
                resultado = cursor.fetchall()
                return resultado if resultado else []  # <- aqui é a correção
        except Exception as e:
            print("Erro ao buscar pódio:", e)
            return []  
        finally:
            conn.close()

def criar_tarefa(titulo, data_tarefa, horario_tarefa, descricao=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO tb_tarefas (titulo, descricao, data_tarefa, horario_tarefa)
                VALUES (%s, %s, %s, %s)
            ''', (titulo, descricao, data_tarefa, horario_tarefa))
            conn.commit()
            print("Tarefa criada com sucesso!")
    except Exception as e:
        print("Erro ao criar tarefa:", e)
    finally:
        conn.close()
