import google.generativeai as genai
import os
import sqlite3
from dotenv import load_dotenv
# Aqui é realizado as importações para realizar




load_dotenv() ## aqui ele carrega a API 
api_key = os.getenv("GEMINI_API_KEY") #Faz a requisição 


if not api_key:
    raise ValueError("API KEY da Gemini não encontrada. Verifique o arquivo .env.") #Caso o campo esteja em branco ou esteja com o caminho errado vai falar que não encontrou

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash") #Realiza a config da API e qual o modelo do Gemini utilizar


chat = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["Você é um cara legal que vai conversar sobre oratória, apresentações e ajudar os alunos, você vai ter a personalidade descolado, jovial e inteligente ao mesmo tempo sendo melhor auxiliador de todos e não vai comentar sobre sexo, drogas, agressão, qualquer coisa ruim você não pode responder pois é um sistema educacional!"]
    }
]) # No código acima é executado antes de começar o prompt, a ordem inicial que a IA vai respeitar e seguir com o que você disse, filtrando o jeito dela


chat = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["Eu quero que se a pessoa fugir muito do assunto você falar que só pode falar coisas realcionadas a ajudar na oratória do aluno tudo bem?"]
    }
]) 

temas_permitidos = ["oratória", "apresentação", "falar em público", "comunicação"] # Aqui foi colocado os filtros e temas principais que vão fazer parte do sistema
palavras_proibidas = ["violência", "política", "arma", "sexo", "drogas"] # Algumas palavras que são proibidas e não podem ser abordadas

def pergunta_permitida(texto): # A função inicia da pergunta permitida
    return True

def resposta_segura(texto):
    return not any(p in texto.lower() for p in palavras_proibidas) # aqui ele vai verificar se o que você escreveu vai possuir respostas proibidas, no caso se isso acontecer ele vai dar um false, caso todas as palavras sejam permitidas ele volta true

def gerar_resposta(pergunta):
    if not pergunta or not pergunta.strip():
        return "❌ Por favor, digite uma pergunta antes de enviar."
    if pergunta_permitida(pergunta) and resposta_segura(pergunta): # Aqui ele verifica se a pergunta foi permitida e faz parte dela ser segura a API vai receber a pergunta do usuario e voltar no returno resposta.text
        try:
            resposta = chat.send_message(pergunta)
            return resposta.text
        except Exception as e:
            return f"❌ Erro ao gerar resposta: {e}" #Caso não funcione ou de algum erro daria esse prompt
    else:
        return "❌ Desculpe, só posso responder perguntas relacionadas à oratória e apresentações." #Se fosse algo proibido ele daria essas frase por conta das restrições configuradas acima
    
    
    


