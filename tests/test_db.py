from unittest.mock import patch, MagicMock
import psycopg2
import os
from scraper.db import save_to_db
from dotenv import load_dotenv

load_dotenv()


def test_save_to_db():
    real_conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )
    mock_conn = MagicMock(wraps=real_conn)
    mock_conn.commit = MagicMock()
    mock_conn.close = MagicMock()

    with patch("psycopg2.connect", return_value=mock_conn):
        cur = real_conn.cursor()

        first_data = {"Junior": {"Python": 1}}
        save_to_db(first_data)
        cur.execute(
            "SELECT date_collected, level, skills FROM jobs WHERE level='Junior' AND date_collected=CURRENT_DATE"
        )
        first_result = cur.fetchone()
        assert first_result is not None
        assert first_result[1] == "Junior"
        assert first_result[2]["Python"] == 1

        second_data = {"Junior": {"Python": 5, "Django": 1}}
        save_to_db(second_data)
        cur.execute(
            "SELECT date_collected, level, skills FROM jobs WHERE level='Junior' AND date_collected=CURRENT_DATE"
        )
        second_result = cur.fetchone()
        assert second_result[1] == "Junior"
        assert second_result[2]["Python"] == 5
        assert second_result[2]["Django"] == 1

        cur.execute(
            "SELECT COUNT(*) FROM jobs WHERE level='Junior' AND date_collected=CURRENT_DATE"
        )
        assert cur.fetchone()[0] == 1

    real_conn.rollback()
    real_conn.close()
