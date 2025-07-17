import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, session
from controller.auth_controller import auth_bp
import smtplib #smtp é o recurso usado para enviar e-mails, criar servers e enviar email
from email.mime.multipart import MIMEMultipart #padrão de envio de mensagem, manda por mime ( codificado )
from email.mime.text import MIMEText #para enviar e-mails com texto
from flask import Flask, render_template, request, redirect, url_for, flash, session

from model import usuario_model  # importa o módulo usuario_model para manipular o banco de dados de ususuarios

from werkzeug.security import generate_password_hash, check_password_hash 


# Adiciona a raiz do projeto ao path ANTES dos imports locais
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from model.chat import gerar_resposta
from controller.auth_controller import auth_bp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_longa_e_aleatoria_para_producao_1234567890'
app.secret_key = 'chave_secreta_segura' 
app.register_blueprint(auth_bp) #registra rotas com blueprint, para manipular com "auth.exemplo", sem problemas



@app.route("/")
def index():
    return render_template("PaginaLogin/PaginaLogin.html")

@app.route("/resposta", methods=["POST", "GET"])
def resposta():
    pergunta = None
    resposta_chatbot = None

    if request.method == "POST":
        pergunta = request.form.get("pergunta")
        if pergunta:
            resposta_chatbot = gerar_resposta(pergunta)

    return render_template("PaginaChatbot/PaginaChatbot.html", pergunta=pergunta, resposta=resposta_chatbot)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)