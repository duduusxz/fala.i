from flask import Blueprint, render_template, redirect, url_for, flash, session
from controller.login_controller import login_required
from model.usuario_model import mostrar_informacoes

auth_bp = Blueprint('auth', __name__)

@conta_bp.route('/minha_conta')
@login_required
def conta():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash("Você precisa estar logado para acessar essa página.")
        return redirect(url_for("login.login"))
    informacoes = mostrar_informacoes(usuario_id)
    return render_template('PaginaConta/PaginaConta.html', informacoes=informacoes)
