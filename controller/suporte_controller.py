from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@suporte_bp.route('/suporte')
def suporte():
    return render_template('PaginaConta/PaginaSuporte.html')

@suporte_bp.route('/termos_config')
def termos_config():
    return render_template('PaginaConta/PaginaTermosConfig.html')

@suporte_bp.route('/feedback')
def feedback():
    return render_template('PaginaConta/PaginaFeedback.html')
