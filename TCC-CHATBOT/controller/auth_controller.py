# controller/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.usuario_model import cadastrar_usuario # Import from the correct location
from model.usuario_model import login_check
from flask import session



auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/cadastro', methods=['GET', 'POST'])


def cadastro():
    if request.method == "POST":
        email = request.form["email"]
        rm = request.form["rm"]
        senha = request.form["senha"]


        if(len (email) < 12 or len (email) > 50): # verifica  a quantidade de caracteres para o cadastro
            msg = "Coisa"
            return msg 
        
        if(len (rm) != 5):
            msg = "Coisa"
            return msg



        sucesso = cadastrar_usuario(email, rm, senha)
        if sucesso:
            flash("Cadastro realizado com sucesso! Faça login.")
            return redirect(url_for("auth.login")) 
        else:
            flash("Erro no cadastro. RM ou e-mail já cadastrados.")
            return render_template("PaginaLogin/PaginaLogin.html")

    return render_template("PaginaLogin")

 
    return render_template('/PaginaLogin/PaginaLogin.html')


#Inicio na pagina de login rota e configuração

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

# Fim da pagina de login rota e configuração

#inicio da pagina de inicio e configuração

@auth_bp.route("/Inicio") 
def deep():
    return render_template("/PaginaInicial/PaginaInicial.html")

# Ffim da pagina de inicio e configuração

#inicio para ver os users
@auth_bp.route('/users')
def user_list():
    # Busca TODOS os usuários do banco de dados
    users = User.query.all()
    # Passa a lista de objetos 'user' para o template
    return render_template('users.html', users=users)


#fim para ver os users


#Começo sistema agenda


@auth_bp.route('/Agenda')
def agenda():
    return render_template('PaginaAgenda/PaginaAgenda.html')

#fim sistema agenda

#inicio termos de uso
@auth_bp.route('/termos')
def termos():
    return render_template('PaginaTermos/PaginaTermos.html')
