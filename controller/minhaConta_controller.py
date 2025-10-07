from flask import Blueprint, render_template, redirect, url_for, flash, session
from controller.login_controller import login_required
from model.usuario_model import mostrar_informacoes

# Cria o Blueprint da "Minha Conta"
minhaConta_bp = Blueprint('minhaConta', __name__, template_folder='../view')

@minhaConta_bp.route('/minha_conta')
@login_required
def minha_conta():
    usuario_id = session.get('usuario_id')

    if not usuario_id:
        flash("Você precisa estar logado para acessar essa página.")
        return redirect(url_for("login.login"))

    informacoes = mostrar_informacoes(usuario_id)
    return render_template('PaginaConta/PaginaMinhaConta.html', informacoes=informacoes)
