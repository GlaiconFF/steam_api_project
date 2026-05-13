from flask import Flask, render_template, request, session, redirect
from scraper.steam_api import choose_game, search_game

app = Flask(__name__)

app.secret_key = "password"

currencies = {"english": "en", "brazilian": "br", "spanish": "es"}

translations = {"english": {
                    "search_placeholder": "Search game",
                    "search_button": "Search",
                    "free_game": "Free to Play"
                },
                "brazilian": {
                    "search_placeholder": "Pesquisar jogo",
                    "search_button": "Pesquisar",
                    "free_game": "Gratuito para Jogar"
                },
                "spanish": {
                    "search_placeholder": "Buscar juego",
                    "search_button": "Buscar",
                    "free_game": "Free to Play"
                }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.context_processor
def inject_translation():

    language = session.get("language", "english")

    return {
        "translation": translations[language]
    }

@app.route("/search")
def search():
    game_name = request.args.get("game_name")
    games_images = choose_game(game_name)
    return render_template("index.html", games_images=games_images)

@app.route("/show_game/<id>")
def show_game(id):

    language = session.get("language", "english")
    currency = currencies[language]
    translation = translations[language]

    game_data = search_game(id, language, currency)
    
    return render_template("index.html", game_data=game_data, translation=translation)

@app.route("/set_language/<language>")
def set_language(language):

    session["language"] = language

    return redirect(request.referrer)

if __name__ == "__main__":
    app.run(debug=True)