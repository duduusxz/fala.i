import sqlite3


#importações necessarias para fazer a requisição do banco e realizar o bycript

def get_db_connection(): #faz a requisição com o banco SQLIte3 que é um banco local
    conn = sqlite3.connect("usuarios.db") #cria o nome do banco ( famoso schema)
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabela(): # cria a tabela de usuarios, que vai conter as informações do user
    with get_db_connection() as conn:
        cursor = conn.cursor() # estabelece conexao
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rm INTEGER UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                pontos INT,
                senha BLOB NOT NULL
            )
        ''')

        cursor.execute('SELECT * FROM usuarios')
        conn.commit()

        resultados = cursor.fetchall()
        print("Usuários cadastrados atualmente:", resultados)
        print("Tabela de usuários criada com sucesso!") # caso a tabela seja criada com sucesso, ele retorna essa mensagem

def cadastrar(rm, email, senha):
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO usuarios (rm, email, senha) VALUES (?, ?, ?)
        ''', (rm, email, senha))
        conn.commit()
    
def buscar_usuario_por_rm_e_email(rm, email):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE rm = ? AND email = ?', (rm, email))
        usuario = cursor.fetchone()
        return dict(usuario) if usuario else None
    
#uma busca mais específica, sendo pelo email para verificar se o email já está cadastrado, especifico no campo 
def buscar_usuario_por_email(email):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario = cursor.fetchone()
        return dict(usuario) if usuario else None
    

def atualizar_senha(email, nova_senha):
    with get_db_connection() as conn:
        conn.execute('UPDATE usuarios SET senha = ? WHERE email = ?', (nova_senha, email)) #Os ? são placeholders para proteger contra SQL Injection.
        conn.commit()
        


def listar_todos_usuarios():
    with get_db_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios')
        usuarios = cursor.fetchall()
        return [dict(usuario) for usuario in usuarios]
    

if __name__ == "__main__":
    criar_tabela()
