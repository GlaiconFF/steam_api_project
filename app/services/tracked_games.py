import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def toggle_tracked_game(game_id):

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    cur = conn.cursor()

    cur.execute(
        """

        SELECT id
        FROM tracked_games
        WHERE game_id = %s

        """,
        (game_id,)
    )

    tracked_game = cur.fetchone()

    if tracked_game:

        cur.execute(
            """

            DELETE FROM tracked_games
            WHERE game_id = %s

            """,
            (game_id,)
        )

        tracked = False

    else:

        cur.execute(
            """

            INSERT INTO tracked_games(game_id)
            VALUES(%s)

            """,
            (game_id,)
        )

        tracked = True

    conn.commit()

    cur.close()

    conn.close()

    return tracked

def is_game_tracked(game_id):

    conn = psycopg2.connect(...)

    cur = conn.cursor()

    cur.execute(
        """

        SELECT id
        FROM tracked_games
        WHERE game_id = %s

        """,
        (game_id,)
    )

    tracked = cur.fetchone() is not None

    cur.close()
    conn.close()

    return tracked