from flask import Blueprint, render_template, request, redirect, url_for, session
from model.usuario_model import criar_tarefa, listar_tarefas
from datetime import datetime

# Corrigido: o blueprint agora é da agenda
agenda_bp = Blueprint('agenda', __name__)

@agenda_bp.route('/agenda', methods=["GET", "POST"])
def agenda():
    if request.method == "POST":
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        data_hora_str = request.form['data_hora']

        data_hora = datetime.fromisoformat(data_hora_str)

        criar_tarefa(titulo, descricao, data_hora)
        return redirect(url_for('agenda.agenda'))  # usa o nome do blueprint certo

    usuario_id = session.get('usuario_id')
    tarefas = listar_tarefas(usuario_id)
    return render_template('PaginaAgenda/PaginaAgenda.html', agenda=tarefas)
