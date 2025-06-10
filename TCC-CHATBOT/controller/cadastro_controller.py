from models.conexao import conectar

def cadastrar_usuario(email, rm, senha):
    conexao = conectar()
    cursor = conexao.cursor()
    
    try:
        sql = "INSERT INTO usuarios (email, rm, senha) VALUES (?, ?, ?)"
        valores = (email, rm, senha)
        cursor.execute(sql, valores)
        conexao.commit()
        return True
    
    except  Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
        return False
    
    finally:
        cursor.close()
        conexao.close()