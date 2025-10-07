from flask import Blueprint, render_template
from model.usuario_model import obter_ranking, buscar_podio

# Cria o Blueprint específico para o ranking
ranking_bp = Blueprint('ranking', __name__)

@ranking_bp.route('/ranking')
def ranking():
    ranking = obter_ranking()
    top3 = buscar_podio()
    restantes = ranking[3:]  # Pega o restante do ranking (depois do top 3)
    return render_template("PaginaRanking/PaginaRanking.html", ranking=ranking, top3=top3, restantes=restantes)
