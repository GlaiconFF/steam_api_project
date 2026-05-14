from flask import Flask
from dotenv import load_dotenv
import os

import psycopg2

load_dotenv()

steam_tags_cache = {
    "english": {},
    "brazilian": {},
    "spanish": {}
}

def load_tags_cache():

    global steam_tags_cache


    with psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port="5432"
    ) as conn:

        with conn.cursor() as cur:

            cur.execute("""
                SELECT steam_tag_id,
                       name_english,
                       name_brazilian,
                       name_spanish
                FROM steam_tags
            """)

            rows = cur.fetchall()

            for row in rows:

                tag_id = row[0]

                steam_tags_cache["english"][tag_id] = row[1]
                steam_tags_cache["brazilian"][tag_id] = row[2]
                steam_tags_cache["spanish"][tag_id] = row[3]

def create_app():

    app = Flask(__name__)

    app.secret_key = os.getenv("APP_SECRET_KEY")

    load_tags_cache()

    from .routes import main
    app.register_blueprint(main)

    return app