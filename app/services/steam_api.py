import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

search_id = "https://store.steampowered.com/api/storesearch/"
item_details = "https://store.steampowered.com/api/appdetails/"
id_reviews = "https://store.steampowered.com/appreviews/"
public_tags = "https://store.steampowered.com/apphoverpublic/"
search_game_tags = "https://store.steampowered.com/search/results/?json=0&tags="

session = requests.Session()

def safe_request_json(url):

    try:
        response = session.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def safe_request_html(url):

    try:
        response = session.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return None

def soup_public_tags(public_tags_html):

    soup = BeautifulSoup(public_tags_html, 'html.parser')

    tags = soup.find_all('div', class_='app_tag')

    game_public_tags_list = [
        tag.text.strip()
        for tag in tags
    ]

    return game_public_tags_list

def soup_search_game_with_tags(search_game_with_tags_html):

    soup = BeautifulSoup(search_game_with_tags_html, 'html.parser')

    games_with_tags = soup.find_all('a', class_='search_result_row')

    games_and_images = {
        game.find('span', class_='title').text: game.find('img')['src']
        for game in games_with_tags
        }

    return games_and_images

def choose_game(name):
    games_datas = {}
    game_to_search = quote(name)

    search_data = safe_request_json(search_id+f"?term={game_to_search}&cc=en&l=en")

    if not search_data:
        return None

    i = 0
    while i < search_data['total']:

        games_datas[search_data['items'][i]['id']] = {'name': search_data['items'][i].get('name', None), 'image': search_data['items'][i].get('tiny_image', None)}
        i += 1

    return games_datas

def search_game_review(game_id, language):

    game_reviews_data = safe_request_json(id_reviews+f"{game_id}?json=1&filter=all&language=all&l={language}")

    return game_reviews_data

def search_game_details(game_id, language, currency):

    game_details_data = safe_request_json(item_details+f"?appids={game_id}&cc={currency}&l={language}")

    return game_details_data

def search_public_tags(game_id, language):
    
    public_tags_data = safe_request_html(public_tags+f"{game_id}?l={language}")
    
    return public_tags_data

def search_game(game_id, language, currency):
    game_reviews_data = search_game_review(game_id, language)
    game_details_data = search_game_details(game_id, language, currency)
    game_public_tags_html = search_public_tags(game_id, language)
    game_public_tags_list = soup_public_tags(game_public_tags_html)

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
        "total_reviews": game_total_reviews,
        "tags_list": game_public_tags_list
        }
    
    return game_dict

def search_game_with_tags(tag_id):

    search_game_with_tags_html = safe_request_html(search_game_tags+tag_id)

    games_found = soup_search_game_with_tags(search_game_with_tags_html)

    return games_found

print(search_game_with_tags("3871"))