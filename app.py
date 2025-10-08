import sys
import os
# Adiciona a raiz do projeto ao path ANTES dos imports locais
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importações de Email (SMTP)
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 

# Importações do Flask
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash 

# NOVO: Importações para Google OAuth
from authlib.integrations.flask_client import OAuth

# Importações de Modelos e Funções
from model import usuario_model 
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


# --- CONFIGURAÇÃO DO FLASK E OAUTH ---

app = Flask(__name__)
# Chave secreta para sessões
app.secret_key = os.environ.get('SECRET_KEY', 'chave_secreta_segura_padrao') 

# Váriaveis de Configuração do Google OAuth 
# É ALTAMENTE RECOMENDADO USAR VARIÁVEIS DE AMBIENTE PARA ISSO!
# Ex: export GOOGLE_CLIENT_ID='seu_id_aqui'
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", '43885387685-llf78in1j7n8tkco2laoao676q04oepf.apps.googleusercontent.com')
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", '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')
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

# Inicializa o objeto OAuth
oauth = OAuth(app)

# Registra o serviço Google
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile' # Escopo para pedir e-mail e nome do usuário
    }
)

# Anexa o objeto oauth ao app para que possa ser acessado nos Blueprints (usando current_app.oauth)
app.oauth = oauth

# --- REGISTRO DE BLUEPRINTS ---

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


# --- ROTAS PRINCIPAIS ---

@app.route("/")
def index():
    # Se o usuário já estiver logado (com Google ou local), redireciona para a página principal
    if 'usuario_id' in session:
        return redirect(url_for('auth.inicio')) 
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
