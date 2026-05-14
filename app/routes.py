from flask import Blueprint, render_template, request, session, redirect
from .services.steam_api import choose_game, search_game
from . import steam_tags_cache

main = Blueprint("main", __name__)

currencies = {"english": "en", "brazilian": "br", "spanish": "es"}

translations = {"english": {
                    "search_placeholder": "Search game",
                    "search_button": "Search",
                    "free_game": "Free to Play",
                    "steam_api_error": "Service Unavailable",
                    "game_name": "Name",
                    "game_description": "Description",
                    "game_price": "Price",
                    "game_supported_languages": "Supported Languages",
                    "game_release_date": "Release Date",
                    "game_positive_reviews": "Positive Reviews",
                    "game_negative_reviews": "Negative Reviews",
                    "game_total_reviews": "Total Reviews",
                    "game_tags": "Tags"
                },
                "brazilian": {
                    "search_placeholder": "Pesquisar jogo",
                    "search_button": "Pesquisar",
                    "free_game": "Gratuito para Jogar",
                    "steam_api_error": "Serviço Indisponível",
                    "game_name": "Nome",
                    "game_description": "Descrição",
                    "game_price": "Preço",
                    "game_supported_languages": "Idiomas Suportados",
                    "game_release_date": "Data de Lançamento",
                    "game_positive_reviews": "Avaliações Positivas",
                    "game_negative_reviews": "Avaliações Negativas",
                    "game_total_reviews": "Total de Avaliações",
                    "game_tags": "Marcadores"
                },
                "spanish": {
                    "search_placeholder": "Buscar juego",
                    "search_button": "Buscar",
                    "free_game": "Free to Play",
                    "steam_api_error": "Servicio No Disponible",
                    "game_name": "Nombre",
                    "game_description": "Descripción",
                    "game_price": "Precio",
                    "game_supported_languages": "Idiomas Admitidos",
                    "game_release_date": "Fecha de Lanzamiento",
                    "game_positive_reviews": "Reseñas Positivas",
                    "game_negative_reviews": "Reseñas Negativas",
                    "game_total_reviews": "Reseñas Totales",
                    "game_tags": "Etiquetas"
                }
}

@main.route("/")
def index():
    return render_template("index.html")

@main.context_processor
def inject_translation():

    language = session.get("language", "english")
    steam_tags = steam_tags_cache[language]

    return {
        "translation": translations[language],
        "steam_tags": steam_tags,
        "show_tags": session.get("show_tags", False)
    }

@main.route("/show_tags")
def show_tags():

    current = session.get("show_tags", False)

    session["show_tags"] = not current

    return redirect("/")

@main.route("/search")
def search():
    game_name = request.args.get("game_name")
    games_datas = choose_game(game_name)

    if not games_datas:
        print("erro")
        return render_template("index.html", error=True)

    return render_template("index.html", games_datas=games_datas)

@main.route("/show_game/<id>")
def show_game(id):

    language = session.get("language", "english")
    currency = currencies[language]

    game_data = search_game(id, language, currency) or {}

    if not game_data:
        return render_template("index.html", error=True)
    
    return render_template("index.html", game_data=game_data)

@main.route("/set_language/<language>")
def set_language(language):

    session["language"] = language

    return redirect(request.referrer)
