import pymysql
from werkzeug.security import generate_password_hash

# settings to generate connections with database
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "12345678",
    "database": "tcc_sql",
     "cursorclass": pymysql.cursors.DictCursor  
    }

def get_db_connection():
    return pymysql.connect(**db_config) # if its all great, return connection correct

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
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('SELECT * FROM usuarios WHERE rm = %s AND email = %s', (rm, email))
            return cursor.fetchone()
    finally:
        conn.close() #close connection

def buscar_usuario_por_email(email): #create function to search just email 
    conn = get_db_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
            return cursor.fetchone()
    finally:
        conn.close() #close connection

def atualizar_senha(email, nova_senha): # create function to to be update password, generating password_hash again, system login perfect !
    nova_senha_hash = generate_password_hash(nova_senha)
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('UPDATE usuarios SET senha = %s WHERE email = %s', (nova_senha, email))
            conn.commit()
    finally:
        conn.close() #here he close connection again

def listar_todos_usuarios(): #function created to list all users
    conn = get_db_connection() #open connection again with bd
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
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
                INSERT INTO tb_tarefas (titulo, descricao, data_tarefa, horario_tarefa VALUES (%s, %s, %s, %s)''', (titulo, descricao, data_tarefa, horario_tarefa))
            conn.commit()
            print("Tarefa criada com sucesso!")
    except Exception as e:
        print("Erro ao criar tarefa:", e)
    finally:
        conn.close() #close connnection
