from flask import Blueprint, render_template, request, redirect, url_for, session
from model.usuario_model import criar_tarefa, listar_tarefas
auth_bp = Blueprint('auth', __name__)



@agenda_bp.route('/agenda', methods=["GET", "POST"])
def agenda():
    if request.method == "POST":
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data_hora_str = request.form['data_hora']

        from datetime import datetime
        data_hora = datetime.fromisoformat(data_hora_str)

        criar_tarefa(titulo, descricao, data_hora)
        return redirect(url_for('agenda.agenda'))

    usuario_id = session.get('usuario_id')
    tarefas = listar_tarefas(usuario_id)
    return render_template('PaginaAgenda/PaginaAgenda.html', agenda=tarefas)
