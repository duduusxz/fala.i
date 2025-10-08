# model/conexao_model.py
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('tcc.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        rm TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        username VARCHAR(30),
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tb_ranking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        pontos INTEGER DEFAULT 0,
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

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

    conn.commit()
    conn.close()

# inicializa automaticamente o banco
init_db()
