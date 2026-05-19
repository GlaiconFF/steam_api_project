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

    CREATE TABLE IF NOT EXISTS tracked_games (

        id SERIAL PRIMARY KEY,

        game_id INTEGER UNIQUE NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )

""")

cur.execute("""

    CREATE TABLE IF NOT EXISTS game_snapshots (

        id SERIAL PRIMARY KEY,

        game_id INTEGER NOT NULL,

        snapshot_date DATE DEFAULT CURRENT_DATE,

        initial_price VARCHAR(50),

        final_price VARCHAR(50),

        discount_percent VARCHAR(10),

        positive_reviews INTEGER,

        negative_reviews INTEGER,

        total_reviews INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )

""")

conn.commit()

cur.close()

conn.close()

print("Tabelas criadas com sucesso!")