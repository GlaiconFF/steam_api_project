import requests
from urllib.parse import quote

search_id = "https://store.steampowered.com/api/storesearch/"
item_details = "https://store.steampowered.com/api/appdetails"
id_reviews = "https://store.steampowered.com/appreviews/"

session = requests.Session()

def safe_request(url):

    try:
        response = session.get(url)
        response.raise_for_status
        return response.json()
    except requests.exceptions.RequestException:
        return None

def choose_game(name):
    games_datas = {}
    game_to_search = quote(name)

    search_data = safe_request(search_id+f"?term={game_to_search}&cc=en&l=en")

    if not search_data:
        return None

    i = 0
    while i < search_data['total']:

        games_datas[search_data['items'][i]['id']] = {'name': search_data['items'][i].get('name', None), 'image': search_data['items'][i].get('tiny_image', None)}
        i += 1

    return games_datas

def search_game_review(game_id, language):

    game_reviews_data = safe_request(id_reviews+f"{game_id}?json=1&filter=all&language=all&l={language}")

    if not game_reviews_data:
        return None

    return game_reviews_data

def search_game_details(game_id, language, currency):

    game_details_data = safe_request(item_details+f"?appids={game_id}&cc={currency}&l={language}")

    if not game_details_data:
        return None

    return game_details_data

def search_game(game_id, language, currency):
    game_reviews_data = search_game_review(game_id, language)
    game_details_data = search_game_details(game_id, language, currency)

    game_positive_reviews = game_reviews_data['query_summary'].get('total_positive')
    game_negative_reviews = game_reviews_data['query_summary'].get('total_negative')
    game_total_reviews = game_reviews_data['query_summary'].get('total_reviews')

    game_header_image = game_details_data[game_id]['data'].get('header_image')
    game_name = game_details_data[game_id]['data'].get('name')
    game_description = game_details_data[game_id]['data'].get('short_description')
    game_is_free = game_details_data[game_id]['data'].get('is_free')
    game_price = game_details_data[game_id]['data'].get('price_overview', {}).get('final_formatted', {})
    game_not_launched = game_details_data[game_id]['data']['release_date'].get('coming_soon')
    game_release_date = game_details_data[game_id]['data']['release_date'].get('date', 0)
    game_supported_languages = game_details_data[game_id]['data'].get('supported_languages', '')
    
    if "*" in game_supported_languages:
        game_supported_languages = game_supported_languages.replace('*','')
    
    if "<b" in game_supported_languages:
        game_supported_languages = game_supported_languages.split("<b")[0]

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