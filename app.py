import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, session



import smtplib #smtp é o recurso usado para enviar e-mails, criar servers e enviar email
from email.mime.multipart import MIMEMultipart #padrão de envio de mensagem, manda por mime ( codificado )
from email.mime.text import MIMEText #para enviar e-mails com texto
from flask import Flask, render_template, request, redirect, url_for, flash, session

from model import usuario_model  # importa o módulo usuario_model para manipular o banco de dados de ususuarios

from werkzeug.security import generate_password_hash, check_password_hash 

#tum tum tum sahur
# Adiciona a raiz do projeto ao path ANTES dos imports locais
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from model.chat import gerar_resposta

# importa todos os blueprints
from controller.aviso_controller import aviso_bp
from controller.suporte_controller import suporte_bp
from controller.agenda_controller import agenda_bp
from controller.cadastro_controller import cadastro_bp
from controller.conta_controller import conta_bp
from controller.feedback_controller import feedback_bp
from controller.login_controller import login_bp
from controller.minhaConta_controller import minhaConta_bp
from controller.ranking_controller import ranking_bp
from controller.senha_controller import senha_bp



app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_longa_e_aleatoria_para_producao_1234567890'
app.secret_key = 'chave_secreta_segura'
 
# registra todos os blueprints
app.register_blueprint(aviso_bp)
app.register_blueprint(suporte_bp)
app.register_blueprint(agenda_bp)
app.register_blueprint(cadastro_bp)
app.register_blueprint(conta_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(login_bp)
app.register_blueprint(minhaConta_bp)
app.register_blueprint(ranking_bp)
app.register_blueprint(senha_bp)


@app.route("/")
def index():
    return render_template("PaginaLogin/PaginaLogin.html") # here he return paginalogin because its route first

@app.route("/resposta", methods=["POST", "GET"]) # here configured for get methods post and get for validation information and verify with database
def resposta():
    pergunta = None
    resposta_chatbot = None

    if request.method == "POST":
        pergunta = request.form.get("pergunta") # he to do request in names that were configured in html
        if pergunta: #if your question is true, he to go valid your question and generate the response
            resposta_chatbot = gerar_resposta(pergunta) # get the craete function

    return render_template("PaginaChatbot/PaginaChatbot.html", pergunta=pergunta, resposta=resposta_chatbot)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port) # configuration the port for start  the project because just to can function after in deploy