# controller/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from model.usuario_model import cadastrar_usuario 
from model.usuario_model import login_check
from flask import session
from flask import Blueprint, render_template, request
from model.chat import gerar_resposta  # importar aqui
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import secrets
from model.usuario_model import salvar_token, validar_token, atualizar_senha_por_email, excluir_token
import os
from dotenv import load_dotenv


load_dotenv()
#importações  para realizar o sistema de autenticação


auth_bp = Blueprint('auth', __name__) # começa a definir o blueprint para autenticação

@auth_bp.route("/")
def index():
    return render_template("PaginaLogin/PaginaLogin.html")

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
        
            print("erro bobao")
        
        if len (rm) < 5 or len (rm) > 5:
            return jsonify({"erro": "RM deve ter exatamente 5 caracteres."})
        
        if len (senha) < 8 or len (senha) > 50:
            return jsonify({"erro": "Senha deve ter entre 8 e 50 caracteres."})
        
        # verifica se a senha e a confirmação de senha são iguais

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
            return render_template("/PaginaInicial/PaginaInicial.html")  # se não for encontrado, retorna erro

    return render_template("PaginaLogin/PaginaLogin.html")

# Fim da pagina de login rota e configuração

# Início do envio de e-mail para redefinição de senha
def enviar_email(destinatario, assunto, corpo_html):
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA")

    msg = MIMEText(corpo_html, "html")
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
            print("E-mail enviado com sucesso.")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)

@auth_bp.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    if request.method == "POST":
        email = request.form["email"]
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=1)

        salvar_token(email, token, expires_at)

        link = url_for("auth.resetar_senha", token=token, _external=True)
        corpo = f"""
        <h2>Redefinição de Senha</h2>
        <p>Clique no link para redefinir sua senha:</p>
        <a href="{link}">Redefinir senha</a><br><br>
        <p>Este link é válido por 1 hora.</p>
        """
        enviar_email(email, "Redefinição de Senha", corpo)
        flash("Um link foi enviado para seu e-mail.")
        return redirect(url_for("auth.login"))

    return render_template("PaginaLogin/EsqueciSenha.html")

@auth_bp.route("/resetar-senha/<token>", methods=["GET", "POST"])
def resetar_senha(token):
    resultado = validar_token(token)
    if not resultado:
        flash("Token inválido ou expirado.")
    

    email, _ = resultado
    if request.method == "POST":
        nova_senha = request.form["senha"]
        confirmar = request.form["confirmarSenha"]
        if nova_senha != confirmar:
            flash("As senhas não coincidem.")
            return render_template("PaginaResetar/PaginaResetar.html", token=token)

        atualizar_senha_por_email(email, nova_senha)
        excluir_token(token)
        
        sucesso = atualizar_senha_por_email(senha)
        
        if sucesso:
          flash("Senha atualizada com sucesso.")
          return redirect(url_for("auth.login"))
        else:
          flash("Erro ao atualizar a senha. Tente novamente.")
          
    

    return render_template("PaginaResetar/PaginaResetar.html", token=token)

#fim do envio de e-mail para redefinição de senha

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


@auth_bp.route("/resposta", methods=["POST", "GET"])
def resposta():
    pergunta = None
    resposta_chatbot = None

    if request.method == "POST":
        pergunta = request.form.get("pergunta")
        if pergunta:
            resposta_chatbot = gerar_resposta(pergunta)

    return render_template("PaginaChatbot/PaginaChatbot.html", pergunta=pergunta, resposta=resposta_chatbot)


#inicia esqueci senha e enviar email


