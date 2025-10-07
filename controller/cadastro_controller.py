from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.security import generate_password_hash
from model import usuario_model  # usado para acessar funções do model

# Cria o Blueprint da parte de cadastro
cadastro_bp = Blueprint('cadastro', __name__, template_folder='../view')

@cadastro_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        rm = request.form["rm"]
        senha = request.form["senha"]
        confirmarSenha = request.form["confirmarSenha"]

        # verifica se a confirmação de senha é igual à senha
        if confirmarSenha != senha:
            flash("Erro: coloque a senha igual.")
            return redirect(url_for("cadastro.cadastro"))

        # validações
        if not (10 <= len(email) <= 40):
            return jsonify({"erro": "Email deve ter entre 10 e 40 caracteres."})
        if len(rm) != 5:
            return jsonify({"erro": "RM deve ter exatamente 5 caracteres."})
        if not (8 <= len(senha) <= 50):
            return jsonify({"erro": "Senha deve ter entre 8 e 50 caracteres."})

        # verifica se já existe um usuário com esse email
        if usuario_model.buscar_usuario_por_email(email):
            flash("Usuário já cadastrado com esse email.")
            return redirect(url_for("cadastro.cadastro"))

        # cria o hash da senha e cadastra o usuário no banco de dados
        senha_hash = generate_password_hash(senha)
        usuario_model.cadastrar(nome, rm, email, senha_hash)

        flash("Usuário cadastrado com sucesso!")
        return redirect(url_for("login.login"))

    return render_template("PaginaCadastro/PaginaCadastro.html")
