import sys
import os
from flask import Flask, session


# Adiciona a raiz do projeto ao path ANTES dos imports locais
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from model.usuario_model import setup_database
from model.chat import gerar_resposta
from controller.auth_controller import auth_bp


app = Flask(__name__)
app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_longa_e_aleatoria_para_producao_1234567890'
app.register_blueprint(auth_bp) #coisas leves haha

# ✅ Chamar a criação do banco/tabela
setup_database()

@app.route("/")
def index():
    return render_template("PaginaLogin/PaginaLogin.html")

@app.route("/resposta", methods=["POST"])
def resposta():
    pergunta = request.form["pergunta"]
    resposta_chatbot = gerar_resposta(pergunta)
    return render_template("PaginaChatbot/PaginaChatbot.html" , pergunta=pergunta, resposta=resposta_chatbot)




if __name__ == "__main__":
    app.run(debug=True)
