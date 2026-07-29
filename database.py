from dotenv import load_dotenv
import os
import psycopg
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():

    print("Connecting to database...")

    conn = psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )

    print("Database connected!")

    return conn