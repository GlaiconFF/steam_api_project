import requests
from urllib.parse import quote

search_id = "https://store.steampowered.com/api/storesearch/"
item_details = "https://store.steampowered.com/api/appdetails"
id_reviews = "https://store.steampowered.com/appreviews/"

session = requests.Session()

def choose_game(name):
    games_images = {}
    game_to_search = quote(name)
    search_id_response = session.get(search_id+f"?term={game_to_search}&cc=en&l=en")
    search_data = search_id_response.json()

    i = 0
    while i < search_data['total']:
        games_images[search_data['items'][i]['id']] = search_data['items'][i].get('tiny_image', None)
        i += 1

    return games_images

def search_game(game_id, language, currency):
    game_reviews_response = session.get(id_reviews+f"{game_id}?json=1&filter=all&language=all&l={language}")
    game_reviews_data = game_reviews_response.json()

    game_positive_reviews = game_reviews_data['query_summary'].get('total_positive')
    game_negative_reviews = game_reviews_data['query_summary'].get('total_negative')
    game_total_reviews = game_reviews_data['query_summary'].get('total_reviews')

    game_details_response = session.get(item_details+f"?appids={game_id}&cc={currency}&l={language}")
    game_data = game_details_response.json()
    game_header_image = game_data[game_id]['data'].get('header_image')
    game_name = game_data[game_id]['data'].get('name')
    game_description = game_data[game_id]['data'].get('short_description')
    game_is_free = game_data[game_id]['data'].get('is_free')
    game_price = game_data[game_id]['data'].get('price_overview', {}).get('final_formatted', {})
    game_not_launched = game_data[game_id]['data']['release_date'].get('coming_soon')
    game_release_date = game_data[game_id]['data']['release_date'].get('date', 0)
    game_supported_languages = game_data[game_id]['data'].get('supported_languages').replace('*','')

    game_dict = {
        "header_image": game_header_image,
        "name": game_name,
        "description": game_description,
        "is_free": game_is_free,
        "price": game_price,
        "not_launched": game_not_launched,
        "release_date": game_release_date,
        "supported_languages": game_supported_languages,
        "positive_reviews": game_positive_reviews,
        "negative_reviews": game_negative_reviews,
        "total_reviews": game_total_reviews
        }
    
    return game_dict