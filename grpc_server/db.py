import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

import psycopg2
import os

def fetch_data(question: str) -> str:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()

    try:
        # Extract all words and convert to lowercase
        words = [word.lower() for word in question.split()]
    
        if not words:
            return None
    
        # Build single WHERE clause for any word match in topic
        conditions = []
        params = []
    
        for word in words:
            conditions.append("topic ILIKE %s")
            like_pattern = f"%{word}%"
            params.append(like_pattern)
    
        # Search in topics and get the corresponding info
        query = """
        SELECT info FROM facts
        WHERE {}
        LIMIT 1;
        """.format(' OR '.join(conditions))
    
        cursor.execute(query, params)
        result = cursor.fetchone()
    
        if result:
            return result[0]
        return None
    
    finally:
        cursor.close()
        conn.close()

def test_connection():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print("[✅] PostgreSQL connected! Version:", version[0])
        cursor.close()
        conn.close()
    except Exception as e:
        print("[❌] Database connection failed:", e)

if __name__ == "__main__":
    test_connection()