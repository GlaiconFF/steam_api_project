import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

cur.execute("""

    SELECT *
    FROM tracked_games

""")

tracked_games = cur.fetchall()

print("\nTRACKED GAMES:\n")

for tracked_game in tracked_games:

    print(tracked_game)

cur.close()

conn.close()