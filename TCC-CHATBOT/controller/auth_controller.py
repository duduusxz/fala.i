# controller/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.usuario_model import cadastrar_usuario # Import from the correct location
from model.usuario_model import login_check
from flask import session



auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        email = request.form["email"]
        rm = request.form["rm"]
        senha = request.form["senha"]

        sucesso = cadastrar_usuario(email, rm, senha)
        if sucesso:
            flash("Cadastro realizado com sucesso! Faça login.")
            return redirect(url_for("auth.login")) 
        else:
            flash("Erro no cadastro. RM ou e-mail já cadastrados.")
            return render_template("PaginaLogin.html")

    return render_template("PaginaLogin")

 
    return render_template('PaginaLogin.html')

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        rm = request.form["rm"]
        senha = request.form["senha"]

        user_id = login_check(rm, email, senha)
        if user_id:
            session["user_id"] = user_id
            return render_template('/PaginaInicial/PaginaInicial.html', user_id=user_id)  # Redireciona para a página de administração ou outra página desejada
        else:
            flash("RM, e-mail ou senha incorretos. Verifique os dados e tente novamente.")

    return render_template("PaginaLogin/PaginaLogin.html")

@auth_bp.route("/Inicio") 
def deep():
    return render_template("/PaginaInicial/PaginaInicial.html")


@auth_bp.route('/users')
def user_list():
    # Busca TODOS os usuários do banco de dados
    users = User.query.all()
    # Passa a lista de objetos 'user' para o template
    return render_template('users.html', users=users)