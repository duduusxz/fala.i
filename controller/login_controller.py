from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from model.usuario_model import cadastrar, buscar_usuario_por_rm_e_email, listar_todos_usuarios
from model.usuario_model import buscar_usuario_por_email  # ou outras funções
from model.usuario_model import obter_ranking  
from model.usuario_model import buscar_podio
from model.usuario_model import mostrar_informacoes
from model.usuario_model import criar_tarefa
from model.usuario_model import listar_tarefas

from model import usuario_model  # Usado para chamar criar_tabela(), se necessário
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import smtplib
from functools import wraps

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



@auth_bp.route("/login", methods=["GET", "POST"])
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

        # Se chegou aqui, login falhou

    return render_template("PaginaLogin/PaginaLogin.html")