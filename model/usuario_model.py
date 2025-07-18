import os # puxar tudo das outras importações
import psycopg2
import psycopg2.extras # Para usar DictCursor com psycopg2
from urllib.parse import urlparse # Para parsear a URL do banco de dados
from werkzeug.security import generate_password_hash # Manter se ainda for usado aqui

# settings to generate connections with database
def get_database_url():
    
    return os.environ.get('DATABASE_URL', 'postgresql://tcc_sql_user:WPhNIdziJ4K6pvYu3dl3XAtAZQmV8rKc@dpg-d1snqure5dus73cdlutg-a.oregon.render.com/tcc_sql_db')

def get_db_connection():
    db_url = get_database_url()

    # Parseia a URL para extrair os componentes (host, user, password, dbname, port)
    result = urlparse(db_url)
    username = result.username
    password = result.password
    database = result.path[1:] # Remove a barra inicial
    hostname = result.hostname
    port = result.port

    try:
        conn = psycopg2.connect(
            host=hostname,
            database=database,
            user=username,
            password=password,
            port=port,
            cursor_factory=psycopg2.extras.DictCursor # Isso faz com que os cursores retornem dicionários
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise # Levanta a exceção para que o app saiba que falhou a conexão



def cadastrar(rm, email, senha_hash): # the function serves to register user in BD, if its possible with password_hash, to upgrade security.
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO usuarios (rm, email, senha) VALUES (%s, %s, %s) 
            ''', (rm, email, senha_hash)) #protect data, to login 
            conn.commit()
    finally:
        conn.close() #close connection

def buscar_usuario_por_rm_e_email(rm, email): #create function to search rm and email
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM usuarios WHERE rm = %s AND email = %s', (rm, email))
            return cursor.fetchone()
    finally:
        conn.close() #close connection

def buscar_usuario_por_email(email): #create function to search just email 
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
            return cursor.fetchone()
    finally:
        conn.close() #close connection

def atualizar_senha(email, nova_senha):
    nova_senha_hash = generate_password_hash(nova_senha)
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
           
            cursor.execute('UPDATE usuarios SET senha = %s WHERE email = %s', (nova_senha_hash, email))
            conn.commit()
    finally:
        conn.close()

def listar_todos_usuarios(): #function created to list all users
    conn = get_db_connection() #open connection again with bd
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM usuarios')
            return cursor.fetchall()
    finally:
        conn.close() #close connection again

def obter_ranking(): #function its very important to search ranking, and compare points of all users in BD 
    conn = get_db_connection()
    try:
            with conn.cursor() as cursor:
                cursor.execute('''
                SELECT nome, pontos FROM tb_ranking ORDER BY pontos DESC;

                ''')
                return cursor.fetchall()
    finally:
                conn.close()    # close connection again

def buscar_podio(): #here he to search your  three first what have more points, and update BD
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
            conn.close() #close connection BD again

def criar_tarefa(titulo, data_tarefa, horario_tarefa, descricao=None): #function created to created task
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO tb_tarefas (titulo, descricao, data_tarefa, horario_tarefa ) VALUES (%s, %s, %s, %s)''', (titulo, descricao, data_tarefa, horario_tarefa))
            conn.commit()
            print("Tarefa criada com sucesso!")
    except Exception as e:
        print("Erro ao criar tarefa:", e)
    finally:
        conn.close() #close connnection
