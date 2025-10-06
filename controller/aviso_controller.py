from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)


@aviso_bp.route('/aviso')
def aviso():
    return render_template('aviso.html')
