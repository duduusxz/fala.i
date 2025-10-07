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

