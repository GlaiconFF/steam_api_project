import requests
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

steam_tags_url = ("https://store.steampowered.com/tagdata/populartags/")

def safe_request_json(url):

    try:

        response = requests.get(url)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException:

        return None

def search_steam_tags(language):

    steam_tags_data = safe_request_json(steam_tags_url + language)

    if not steam_tags_data:
        return {}

    return {
        item['tagid']: item['name']
        for item in steam_tags_data
    }

def save_tags_to_db():

    english_tags = search_steam_tags("english")

    brazilian_tags = search_steam_tags("brazilian")

    spanish_tags = search_steam_tags("spanish")

    with psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port="5432"
    ) as conn:

        with conn.cursor() as cur:

            cur.execute("""
                CREATE TABLE IF NOT EXISTS steam_tags (

                    steam_tag_id INTEGER PRIMARY KEY,

                    name_english VARCHAR(100),

                    name_brazilian VARCHAR(100),

                    name_spanish VARCHAR(100)
                )
            """)

            for tag_id in english_tags.keys():

                cur.execute(
                    """
                    INSERT INTO steam_tags(

                        steam_tag_id,

                        name_english,

                        name_brazilian,

                        name_spanish
                    )

                    VALUES(%s, %s, %s, %s)

                    ON CONFLICT (steam_tag_id)

                    DO NOTHING
                    """,
                    (
                        tag_id,

                        english_tags.get(tag_id),

                        brazilian_tags.get(tag_id),

                        spanish_tags.get(tag_id)
                    )
                )

    print("Tags salvas com sucesso!")

#save_tags_to_db()
