# model/usuario_model.py
from werkzeug.security import generate_password_hash
from model.conexao_model import get_db_connection


def cadastrar(nome, rm, email, senha_hash):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nome, rm, email, senha)
            VALUES (?, ?, ?, ?)
        ''', (nome, rm, email, senha_hash))
        conn.commit()
    finally:
        conn.close()

def buscar_usuario_por_rm_e_email(rm, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE rm = ? AND email = ?', (rm, email))
    user = cursor.fetchone()
    conn.close()
    return user

def buscar_usuario_por_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def atualizar_senha(email, nova_senha):
    nova_senha_hash = generate_password_hash(nova_senha)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET senha = ? WHERE email = ?', (nova_senha_hash, email))
    conn.commit()
    conn.close()

def listar_todos_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios


def mostrar_informacoes(usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, rm, email FROM usuarios WHERE id = ?", (usuario_id,))
    info = cursor.fetchone()
    conn.close()
    return info





