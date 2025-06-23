import sqlite3
import bcrypt

#importações necessarias para fazer a requisição do banco e realizar o bycript

def get_db_connection(): #faz a requisição com o banco SQLIte3 que é um banco local
    conn = sqlite3.connect("database.db") #cria o nome do banco ( famoso schema)
    conn.row_factory = sqlite3.Row

    
    return conn


def setup_database(): # cria a tabela de usuarios, que vai conter as informações do user
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
        conn.commit()

def cadastrar_usuario(email, rm,  password):
    if not rm or not email or not password:
        return False 
    
    #aqui a funcao de cadastrar usuario se ele nao inserir no banco esses dados ele da erro e retorna falso
    
    
    try: # ele vai executar uma vez o codigo em bycript, vai gerar o hash da senha ( criptografar a senha para segunraça)
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        with get_db_connection() as conn: # faz a conexao do banco 
            conn.execute("INSERT INTO usuarios (rm, email, senha) VALUES (?, ?, ?)", (rm, email, hashed))
            #acima ele insere os dados dando o INSERT, já com a senha em hash para vir em cripto
        return True # se der tudo certo da true
    except sqlite3.IntegrityError:
        return False # se não ele retorna erro do banco (Igual com o SQlExcpetion do java que já utilizei)
    
    
    
def login_check(rm, email, password): # faz a verificação do user, faz a conexao e verifica se o dado que a pessoa inseriu condiz com que ela verifica
    try: 
        with get_db_connection() as conn:
         user = conn.execute(
            "SELECT id, senha FROM usuarios WHERE rm = ? AND email = ?", (rm, email)
            ).fetchone()
    
        if user and bcrypt.checkpw(password.encode(), user['senha']): # faz essa vericiação da senha separada e checa com o hash criado
           return user['id'] # se der tudo certo retorna o ID do user cadastrado
        return None

    except Exception as e: # caso nao retornar o ID do user , que é criado no insert, ele não executa mais
        return None
