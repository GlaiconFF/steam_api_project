from flask import Flask, render_template, request
from scraper.steam_api import choose_game, search_game

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    game_name = request.args.get("game_name")
    games_images = choose_game(game_name)
    return render_template("index.html", games_images=games_images)

@app.route("/show_game/<id>")
def show_game(id):
    game_data = search_game(id)
    return render_template("index.html", game_data=game_data)

if __name__ == "__main__":
    app.run(debug=True)