from flask import Blueprint, render_template, request, session, redirect
from .services.steam_api import choose_game, search_game
from . import steam_tags_cache

main = Blueprint("main", __name__)

currencies = {
    "english": "en",
    "brazilian": "br",
    "spanish": "es"
}

translations = {
    "english": {
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
        "game_tags": "Tags",
        "search_tag": "Search tag..."
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
        "game_tags": "Marcadores",
        "search_tag": "Pesquisar marcador..."
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
        "game_tags": "Etiquetas",
        "search_tag": "Buscar etiqueta..."
    }
}


@main.context_processor
def inject_translation():

    language = session.get("language", "english")

    return {
        "translation": translations[language],
        "steam_tags": steam_tags_cache[language],
        "selected_tags": session.get("selected_tags", [])
    }


@main.route("/")
def index():
    return render_template("index.html")

@main.route("/toggle_tag/<int:tag_id>")
def toggle_tag(tag_id):

    selected = session.get("selected_tags", [])

    if tag_id in selected:
        selected.remove(tag_id)
    else:
        selected.append(tag_id)

    session["selected_tags"] = selected

    return ""


@main.route("/search")
def search():
    game_name = request.args.get("game_name")
    games_datas = choose_game(game_name)

    if not games_datas:
        return render_template("index.html", error=True)

    return render_template("index.html", games_datas=games_datas)


@main.route("/show_game/<id>")
def show_game(id):

    language = session.get("language", "english")
    currency = currencies[language]

    game_data = search_game(id, language, currency) or {}

    if not game_data:
        return render_template("index.html", error=True)

    steam_tags = steam_tags_cache[language]

    tag_name_to_id = {
        tag_name: tag_id
        for tag_id, tag_name in steam_tags.items()
    }

    game_data["tags_with_id"] = []

    for game_tag in game_data["tags_list"]:

        tag_id = tag_name_to_id.get(game_tag)

        game_data["tags_with_id"].append({
            "id": tag_id,
            "name": game_tag
        })

    return render_template("index.html", game_data=game_data)

@main.route("/set_language/<language>")
def set_language(language):

    session["language"] = language
    session.modified = True
    return redirect(request.referrer or "/")