# controller/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.usuario_model import cadastrar_usuario 
from model.usuario_model import login_check
from flask import session
import sqlite3
import bcrypt


#importações  para realizar o sistema de autenticação


auth_bp = Blueprint('auth', __name__) # começa a definir o blueprint para autenticação

@auth_bp.route('/cadastro', methods=['GET', 'POST'])  # define nessa linha a rota de cadastro, que vai pegar as informações do usuário e postar no form
def cadastro():
    if request.method == "POST":
        email = request.form["email"]
        rm = request.form["rm"]
        senha = request.form["senha"]  # pega os dados do formulário de cadastro para verificar
        confirmarSenha = request.form["confirmarSenha"]  # pega a confirmação de senha do formulário
        
        if confirmarSenha != senha:  # verifica se a confirmação de senha é igual à senha
            return render_template("aviso.html", erro="As senhas não coincidem.")  # se não for igual, retorna erro

        
        
        if len (email ) < 10 or len (email) > 40:
            return jsonify({"erro": "Email deve ter entre 10 e 40 caracteres."})  # verifica se o email, rm e senha estão dentro dos limites de caracteres
        
            
        
        if len (rm) < 5 or len (rm) > 5:
            return jsonify({"erro": "RM deve ter exatamente 5 caracteres."})
        
        if len (senha) < 8 or len (senha) > 50:
            return jsonify({"erro": "Senha deve ter entre 8 e 50 caracteres."})
        
        # verifica se a senha e a confirmação de senha são iguais


        sucesso = cadastrar_usuario(email, rm, senha)
 # se der sucesso com o cadastro, chama a função cadastrar_usuario do model.usuario_model
        # que vai inserir os dados no banco de dados
        if sucesso:
            flash("Cadastro realizado com sucesso! Faça login.") # se for sucesso vai exibir msg e mandar vc para outra página ( Login)
            return redirect(url_for("auth.login")) 
        else:
            flash("Erro no cadastro. RM ou e-mail já cadastrados.") # caso dê erro, exibe msg de erro
            return render_template("PaginaLogin/PaginaLogin.html")

    return render_template("PaginaCadastro/PaginaCadastro.html") # aqui rennderiza a página de cadastro, que é a PaginaLogin.html ( Ambas estão juntas no template)

 
    return render_template('PaginaLogin/PaginaLogin.html')


#Inicio na pagina de login rota e configuração

@auth_bp.route("/login", methods=["GET", "POST"])
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
            flash("RM, e-mail ou senha incorretos.") # se não for encontrado, retorna erro

    return render_template("PaginaLogin/PaginaLogin.html")

# Fim da pagina de login rota e configuração

#inicio da pagina de inicio e configuração



# Ffim da pagina de inicio e configuração

#inicio para ver os users
@auth_bp.route('/users')
def user_list():
    # Busca TODOS os usuários do banco de dados
    users = User.query.all() 
    # Passa a lista de objetos "user" para o template
    return render_template('users.html', users=users) # vai renderizar a página de usuários, que é a users.html 


#fim para ver os users

@auth_bp.route('/inicio') # rota definida para a página inicial 
def inicio():
    return render_template('PaginaInicial/PaginaInicial.html')

#Começo sistema agenda



@auth_bp.route('/agenda')  # rota definida para a página de agenda
def agenda():
    return render_template('PaginaAgenda/PaginaAgenda.html')

#fim sistema agenda


#inicio termos de uso

@auth_bp.route('/termos')  # rota definida para a página de termos de uso
def termos():
    return render_template('PaginaTermos/PaginaTermos.html')

#fim dos termos


#inicio da minha conta

@auth_bp.route('/minha_conta')
def conta():
    return render_template('PaginaConta/PaginaConta.html')

# fim minha conta

# rota aviso

@auth_bp.route('/aviso')
def aviso():
    return render_template('aviso.html')

#rota para ranking
@auth_bp.route('/ranking')
def ranking():   #essa funcao vai apenas mostrar o ranking com base no banco de dados

    jogadores = [
        {"Nome": "Livia", "Pontos": 160},
        {"Nome": "Livia", "Pontos": 190},
        {"Nome": "Livia", "Pontos": 180},
    ]  #criado um array para representar basicamento o banco de dados que vai possuir, com cada jogador e a sua quantidade de pontos

    for i, nome in enumerate(jogadores, start=1): # aqui ele vai percorrer a lista de jogadores, enumerando elas 
        print(f"{i}º lugar: {jogadores['nome']} - {jogadores['pontos']} pontos") # aqui ele vai printar o ranking

    
    return render_template('ranking.html')


# aqui se inicia uma outra funçao que vai fazer a verificação e order by no ranking

def verificar():
    return None

# inicio rota esqueci a senha
@auth_bp.route('/esqueci_senha')
def esqueci_senha():
    return render_template('PaginaEsqueciSenha/PaginaEsqueciSenha.html')