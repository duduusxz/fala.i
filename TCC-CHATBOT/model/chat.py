import google.generativeai as genai
import os
from dotenv import load_dotenv

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conexao import conectar

# === Configuração inicial ===
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API KEY da Gemini não encontrada. Verifique o arquivo .env.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[
    {"role": "user", "parts": ["Você é um cara legal que vai conversar sobre oratória, apresentações..."]}
])

temas_permitidos = ["oratória", "apresentação", "falar em público", "comunicação"]
palavras_proibidas = ["violência", "política", "arma", "sexo", "drogas"]

# === Funções auxiliares ===
def pergunta_permitida(texto):
    return True  # Personalize se quiser limitar os temas

def resposta_segura(texto):
    return not any(p in texto.lower() for p in palavras_proibidas)

def salvar_mensagem(autor, mensagem):
    conexao = conectar()
    with conexao.cursor() as cursor:
        sql = "INSERT INTO historico (autor, mensagem) VALUES (%s, %s)"
        cursor.execute(sql, (autor, mensagem))
        conexao.commit()
    conexao.close()

def obter_historico():
    conexao = conectar()
    with conexao.cursor() as cursor:
        cursor.execute("SELECT autor, mensagem, timestamp FROM historico ORDER BY id ASC")
        mensagens = cursor.fetchall()
    conexao.close()
    return mensagens

def limpar_historico():
    conexao = conectar()
    with conexao.cursor() as cursor:
        cursor.execute("DELETE FROM historico")
        conexao.commit()
    conexao.close()

def gerar_resposta(pergunta):
    if not pergunta.strip():
        return "❌ Por favor, digite uma pergunta antes de enviar."
    
    salvar_mensagem("Usuário", pergunta)

    if pergunta_permitida(pergunta) and resposta_segura(pergunta):
        try:
            resposta = chat.send_message(pergunta)
            salvar_mensagem("IA", resposta.text)
            return resposta.text
        except Exception as e:
            erro = f"❌ Erro ao gerar resposta: {e}"
            salvar_mensagem("IA", erro)
            return erro
    else:
        aviso = "❌ Só posso responder perguntas sobre oratória e apresentações."
        salvar_mensagem("IA", aviso)
        return aviso

def mostrar_historico():
    print("\n📜 Histórico da conversa:")
    for msg in obter_historico():
        print(f"[{msg['timestamp']}] {msg['autor']}: {msg['mensagem']}")

# === Execução ===
while True:
    pergunta = input("\nVocê: ")
    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("🛑 Encerrando o chat.")
        break
    elif pergunta.lower() == "limpar":
        limpar_historico()
        print("🧹 Histórico apagado.")
        continue

    resposta = gerar_resposta(pergunta)
    print(f"IA: {resposta}")
    mostrar_historico()


