import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "meu_banco.db"  # nome do arquivo que vai guardar os dados

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao SQLite: {e}")
        raise

def cadastrar(rm, email, senha_hash):
    conn = get_db_connection()
    try:
        with conn:
            conn.execute('INSERT INTO usuarios (rm, email, senha) VALUES (?, ?, ?)', 
                         (rm, email, senha_hash))
    finally:
        conn.close()

def buscar_usuario_por_rm_e_email(rm, email):
    conn = get_db_connection()
    try:
        cursor = conn.execute('SELECT * FROM usuarios WHERE rm = ? AND email = ?', (rm, email))
        return cursor.fetchone()
    finally:
        conn.close()

def buscar_usuario_por_email(email):
    conn = get_db_connection()
    try:
        cursor = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        return cursor.fetchone()
    finally:
        conn.close()

def atualizar_senha(email, nova_senha):
    nova_senha_hash = generate_password_hash(nova_senha)
    conn = get_db_connection()
    try:
        with conn:
            conn.execute('UPDATE usuarios SET senha = ? WHERE email = ?', 
                         (nova_senha_hash, email))
    finally:
        conn.close()

def listar_todos_usuarios():
    conn = get_db_connection()
    try:
        cursor = conn.execute('SELECT * FROM usuarios')
        return cursor.fetchall()
    finally:
        conn.close()

def obter_ranking():
    conn = get_db_connection()
    try:
        cursor = conn.execute('SELECT nome, pontos FROM tb_ranking ORDER BY pontos DESC')
        return cursor.fetchall()
    finally:
        conn.close()

def buscar_podio():
    conn = get_db_connection()
    try:
        cursor = conn.execute('SELECT * FROM tb_ranking ORDER BY pontos DESC LIMIT 3')
        resultado = cursor.fetchall()
        return resultado if resultado else []
    except Exception as e:
        print("Erro ao buscar pódio:", e)
        return []
    finally:
        conn.close()

def criar_tarefa(titulo, data_tarefa, horario_tarefa, descricao=None):
    conn = get_db_connection()
    try:
        with conn:
            conn.execute('''
                INSERT INTO tb_tarefas (titulo, descricao, data_tarefa, horario_tarefa) 
                VALUES (?, ?, ?, ?)
            ''', (titulo, descricao, data_tarefa, horario_tarefa))
            print("Tarefa criada com sucesso!")
    except Exception as e:
        print("Erro ao criar tarefa:", e)
    finally:
        conn.close()

        
