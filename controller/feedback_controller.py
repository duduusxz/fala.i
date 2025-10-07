from flask import Blueprint, render_template

# Criação do Blueprint para o feedback
feedback_bp = Blueprint('feedback', __name__, template_folder='../view')

@feedback_bp.route('/feedback')
def feedback():
    return render_template('PaginaConta/PaginaFeedback.html')

    