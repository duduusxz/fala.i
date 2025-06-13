# controller/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.usuario_model import cadastrar_usuario 
from model.usuario_model import login_check
from flask import session

#importações  para realizar o sistema de autenticação


auth_bp = Blueprint('auth', __name__) # começa a definir o blueprint para autenticação

@auth_bp.route('/cadastro', methods=['GET', 'POST'])  # define nessa linha a rota de cadastro, que vai pegar as informações do usuário e postar no form
def cadastro():
    if request.method == "POST":
        email = request.form["email"]
        rm = request.form["rm"]
        senha = request.form["senha"] # pega os dados do formulário de cadastro para verificar
        
        if len (email ) < 10 or len (email) > 40:
            return jsonify({"erro": "Email deve ter entre 10 e 40 caracteres."})  # verifica se o email, rm e senha estão dentro dos limites de caracteres
        
            print("erro bobao")
        
        if len (rm) < 5 or len (rm) > 5:
            return jsonify({"erro": "RM deve ter exatamente 5 caracteres."})
        
        if len (senha) < 8 or len (senha) > 50:
            return jsonify({"erro": "Senha deve ter entre 8 e 50 caracteres."})

        sucesso = cadastrar_usuario(email, rm, senha) # se der sucesso com o cadastro, chama a função cadastrar_usuario do model.usuario_model
        # que vai inserir os dados no banco de dados
        if sucesso:
            flash("Cadastro realizado com sucesso! Faça login.") # se for sucesso vai exibir msg e mandar vc para outra página ( Login)
            return redirect(url_for("auth.login")) 
        else:
            flash("Erro no cadastro. RM ou e-mail já cadastrados.") # caso dê erro, exibe msg de erro
            return render_template("PaginaLogin/PaginaLogin.html")

    return render_template("PaginaLogin") # aqui rennderiza a página de cadastro, que é a PaginaLogin.html ( Ambas estão juntas no template)

 
    return render_template('PaginaLogin/PaginaLogin.html')


@auth_bp.route("/login", methods=["GET", "POST"]) # Aqui defini a rota de login, que vai pegar as informações que está salva no banco de dados cadastrado e verificar nessa rota 
def login():
    if request.method == "POST":
        email = request.form["email"]
        rm = request.form["rm"]
        senha = request.form["senha"] # pega os dados do formulário de login para verificar
        # Verifica se o usuário existe e a senha está correta ( Ambos criados no banco UsuarioModel)

        user_id = login_check(rm, email, senha) # chama a função login_check do model.usuario_model, que vai verificar se o usuário existe e se a senha está correta
        # Se o usuário for encontrado, user_id será o ID do usuário, caso contrário será None ( Cada cadastrado possui o seu ID unico)
        if user_id:
            session["user_id"] = user_id 
            return render_template('/PaginaInicial/PaginaInicial.html', user_id=user_id)  ##se estiver correto vai pra page inicial
        else:
            flash("RM, e-mail ou senha incorretos. Verifique os dados e tente novamente.") # se nao estiver vai alertar que deu erro

    return render_template("PaginaLogin/PaginaLogin.html")



@auth_bp.route("/Inicio")  # rota definida para a página inicial
def deep():
    return render_template("/PaginaInicial/PaginaInicial.html")


@auth_bp.route('/users') # rota definida para listar os usuários e ver todos por conta do SQLite3
def user_list():
    # Busca TODOS os usuários do banco de dados
    users = User.query.all() 
    # Passa a lista de objetos "user" para o template
    return render_template('users.html', users=users) # vai renderizar a página de usuários, que é a users.html


# fim

@auth_bp.route('Inicio') # rota definida para a página inicial 
def inicio():
    return render_template('PaginaInicial/PaginaInicial.html')

#Começo sistema agenda



@auth_bp.route('/Agenda')  # rota definida para a página de agenda
def agenda():
    return render_template('PaginaAgenda/PaginaAgenda.html')


#fim agenda 

#inicio pagina termos

@auth_bp.route('/termos') # rota definida para a página de termos
def termos():
    return render_template('PaginaTermos/PaginaTermos.html')
