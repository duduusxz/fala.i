from flask import Blueprint, render_template, request, redirect, url_for, session
from model.agenda_model import criar_tarefa, listar_tarefas
from datetime import datetime

agenda_bp = Blueprint('agenda', __name__)  # certifique de registrar no app.py

@agenda_bp.route('/agenda', methods=["GET", "POST"])
def agenda():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('auth.login'))  # ou qualquer rota de login que você tenha

    if request.method == "POST":
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data_hora_str = request.form['data_hora']
        data_hora = datetime.fromisoformat(data_hora_str)

        criar_tarefa(titulo, descricao, data_hora)
        return redirect(url_for('agenda.agenda'))

    tarefas = listar_tarefas(usuario_id)
    return render_template('PaginaAgenda/PaginaAgenda.html', agenda=tarefas)