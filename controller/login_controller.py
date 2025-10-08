from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from model import usuario_model

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        rm = request.form["rm"]
        senha = request.form["senha"]

        usuario = usuario_model.buscar_usuario_por_rm_e_email(rm, email)

        if usuario:
            senha_hash = usuario['senha']
            if isinstance(senha_hash, bytes):
                senha_hash = senha_hash.decode('utf-8')

            if check_password_hash(senha_hash, senha):
                session['usuario_id'] = usuario['id']
                session['usuario_email'] = usuario['email']
                session['usuario_rm'] = usuario['rm']
                flash("Login realizado com sucesso!")
                return redirect(url_for('auth.inicio'))

        flash("Credenciais inválidas. Verifique RM, email ou senha.")
        
    return render_template("PaginaLogin/PaginaLogin.html")

# NOVO: Rota para iniciar o login com Google
@login_bp.route('/login/google')
def login_google():
    # Acessa o objeto OAuth registrado no app principal
    oauth = current_app.oauth
    
    # Define a URL de callback que o Google usará para nos retornar
    redirect_uri = url_for('login.google_auth', _external=True)
    
    # Redireciona o usuário para a página de login do Google
    return oauth.google.authorize_redirect(redirect_uri)


# NOVO: Rota de Callback (Retorno do Google)
@login_bp.route('/google/auth')
def google_auth():
    oauth = current_app.oauth
    
    try:
        # Tenta obter o token e as informações do usuário
        token = oauth.google.authorize_access_token()
        user_info = oauth.google.parse_id_token(token)

        # 1. Extrair dados
        email = user_info.get('email')
        name = user_info.get('name')
        google_id = user_info.get('sub') # ID exclusivo do Google
        
        # 2. Lógica de Registro/Login no seu BD
        usuario = usuario_model.buscar_usuario_por_email(email)
        
        if not usuario:
            # Novo usuário: registra no BD (Você precisará criar esta função no seu model!)
            # Se você usa RM, pode ser necessário que o usuário complete o cadastro após o login inicial
            # Por simplicidade, vou logar apenas com o que o Google deu:
            
            # --- NOVO TRECHO (Adapte ao seu modelo!) ---
            novo_usuario_id = usuario_model.criar_usuario_google(email, name, google_id)
            session['usuario_id'] = novo_usuario_id
            session['usuario_email'] = email
            # Não terá RM se você não pedir na primeira vez
            # ------------------------------------------

        else:
            # Usuário existente: apenas loga
            session['usuario_id'] = usuario['id']
            session['usuario_email'] = usuario['email']
            session['usuario_rm'] = usuario.get('rm') # Pega o RM se existir
        
        flash(f"Login com Google realizado com sucesso, {name}!")
        return redirect(url_for('auth.inicio')) # Redireciona para sua página inicial

    except Exception as e:
        # Tratamento de erro (ex: usuário cancelou o login, erro de token)
        print(f"Erro ao processar login com Google: {e}")
        flash("Falha ao entrar com Google. Tente novamente.")
        return redirect(url_for('login.login'))

from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Você precisa estar logado para acessar essa página.")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)
    return decorated_function

