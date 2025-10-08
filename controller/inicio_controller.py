from flask import Blueprint, render_template, session, flash, redirect, url_for

# Cria o blueprint do início
inicio_bp = Blueprint('inicio', __name__)

# Rota da página inicial
@inicio_bp.route('/inicio')
def inicio():
    # Se quiser verificar login, descomente o bloco abaixo:
    # if 'usuario_id' not in session:
    #     flash("Você precisa fazer login primeiro.")
    #     return redirect(url_for('auth.login'))

    # Renderiza a página inicial
    # Se quiser passar dados do usuário da sessão:
    # return render_template(
    #     'PaginaInicial/PaginaInicial.html',
    #     usuario_email=session.get('usuario_email'),
    #     usuario_rm=session.get('usuario_rm')
    # )
    
    # Versão simples sem dados da sessão
    return render_template('PaginaInicial/PaginaInicial.html')