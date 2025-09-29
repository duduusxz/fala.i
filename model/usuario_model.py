import sqlite3
from werkzeug.security import generate_password_hash

def get_db_connection():
    """
    Cria conexão com o banco SQLite
    O arquivo 'tcc.db' será criado automaticamente
    """
    conn = sqlite3.connect('tcc.db')
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn

def init_db():
    """
    Inicializa o banco de dados com todas as tabelas necessárias
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rm TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    

    # Tabela de ranking
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tb_ranking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        pontos INTEGER DEFAULT 0,
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabela de tarefas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tb_tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        data_tarefa DATE NOT NULL,
        horario_tarefa TIME NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    
    cursor.execute("INSERT INTO tb_ranking (nome, pontos) VALUES ('andre', '234')")
    cursor.execute("INSERT INTO tb_ranking (nome, pontos) VALUES ('bruno', '444')")
    cursor.execute("INSERT INTO tb_ranking (nome, pontos) VALUES ('carlos', '555')")    

    conn.commit()
    conn.close()
    print("inicializei o banco")

# Exemplo de uso para testar a conexão
def testar_conexao():
    try:
        init_db()  # Garante que as tabelas existem
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Listar tabelas do banco
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("Tabelas no banco de dados:")
        for table in tables:
            print(f" - {table['name']}")
        
        cursor.close()
        connection.close()
        print("conexao fechoy")
        
    except Exception as e:
        print(" erro banco {e}")

def cadastrar(rm, email, senha_hash):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (rm, email, senha) VALUES (?, ?, ?)
        ''', (rm, email, senha_hash))
        conn.commit()
        
    except sqlite3.IntegrityError:
        print("RM ou email já existem!")
        raise
    finally:
        conn.close()

def buscar_usuario_por_rm_e_email(rm, email):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE rm = ? AND email = ?', (rm, email))
        return cursor.fetchone()
    finally:
        conn.close()

def buscar_usuario_por_email(email):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        return cursor.fetchone()
    finally:
        conn.close()

def atualizar_senha(email, nova_senha):
    nova_senha_hash = generate_password_hash(nova_senha)
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET senha = ? WHERE email = ?', (nova_senha_hash, email))
        conn.commit()
    finally:
        conn.close()

def listar_todos_usuarios():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios')
        return cursor.fetchall()
    finally:
        conn.close()

def obter_ranking():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT nome, pontos FROM tb_ranking ORDER BY pontos DESC')
        return cursor.fetchall()
    finally:
        conn.close()

def mostrar_informacoes(usuario_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT rm, email FROM usuarios WHERE id = ?", (usuario_id,))
        return cursor.fetchone()
    finally:
        conn.close()

def buscar_podio():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tb_ranking ORDER BY pontos DESC LIMIT 3")
        resultado = cursor.fetchall()
        return resultado if resultado else []
    except Exception as e:
        print("Erro ao buscar pódio:", e)
        return []  
    finally:
        conn.close()

def listar_tarefas(usuario_id): #comecando a listar as tarefas pelo proprio ID, espernado o java terminar a parte dele
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tb_tarefas")
    tarefas = cursor.fetchall()
    conn.close()
    print("Tarefas no banco:", tarefas)  # <-- debug
    return tarefas

    

def criar_tarefa(titulo, data_tarefa, horario_tarefa, descricao=None):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tb_tarefas (titulo, descricao, data_tarefa, horario_tarefa) 
            VALUES (?, ?, ?, ?)
        ''', (titulo, descricao, data_tarefa, horario_tarefa))
        conn.commit()
        print("Tarefa criada com sucesso!")  # <-- vai aparecer no terminal
    except Exception as e:
        print("Erro ao criar tarefa:", e)
        raise
    finally:
        conn.close()





# Inicializa o banco automaticamente quando o módulo é importado
init_db()



# Teste opcional
if __name__ == "__main__":
    testar_conexao()