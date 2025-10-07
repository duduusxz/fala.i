from flask import Blueprint, render_template

aviso_bp = Blueprint('aviso', __name__)

@aviso_bp.route('/aviso')
def aviso():
    return render_template('aviso.html')


