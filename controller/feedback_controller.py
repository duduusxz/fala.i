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

@auth_bp.route('/feedback')
def feedback():

    return render_template('PaginaConta/PaginaFeedback.html')

    