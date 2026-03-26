import json
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def save_to_db(data: dict):
    for level, skill in data.items():
        print(level, skill)

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB_NAME"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
        )
        cur = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            date_collected DATE DEFAULT CURRENT_DATE,
            level VARCHAR(50),
            skills JSONB,
            UNIQUE(date_collected, level)
        );
        """
        cur.execute(create_table_query)

        update_query = """
            INSERT INTO jobs (level, skills)
            VALUES (%s, %s)
            ON CONFLICT (date_collected, level)
            DO UPDATE SET skills = EXCLUDED.skills
        """

        for level, skills_dict in data.items():
            if not skills_dict:
                continue
            skills_json_ser = json.dumps(skills_dict)
            cur.execute(update_query, (level, skills_json_ser))

        conn.commit()
        print("Saved to DataBase is successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error to DataBase: {error}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
