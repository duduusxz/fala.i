# model/tarefa_model.py
from model.conexao_model import get_db_connection

def listar_tarefas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_tarefas')
    tarefas = cursor.fetchall()
    conn.close()
    return tarefas

def criar_tarefa(titulo, data_tarefa, horario_tarefa, descricao=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tb_tarefas (titulo, descricao, data_tarefa, horario_tarefa)
        VALUES (?, ?, ?, ?)
    ''', (titulo, descricao, data_tarefa, horario_tarefa))
    conn.commit()
    conn.close()
