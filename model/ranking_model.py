# model/ranking_model.py
from model.conexao_model import get_db_connection

def obter_ranking():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT nome, pontos FROM tb_ranking ORDER BY pontos DESC')
    ranking = cursor.fetchall()
    conn.close()
    return ranking

def buscar_podio():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_ranking ORDER BY pontos DESC LIMIT 3')
    podio = cursor.fetchall()
    conn.close()
    return podio
