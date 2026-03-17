import psycopg2
from datetime import datetime

def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="ivandarlami",
        password="password",
        host="localhost"
    )

def save_price(coin_name, price):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prices(
            id SERIAL PRIMARY KEY,
            coin_name TEXT,
            price FLOAT,
            timestamp TIMESTAMP
        )            
    """)
    
    cur.execute(
        "INSERT INTO prices(coin_name, price, timestamp) VALUES (%s, %s, %s)",
        (coin_name, price, datetime.now())
    )
    
    conn.commit()
    cur.close()
    conn.close()

def get_price_history(coin_name, limit=10):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "SELECT * FROM prices WHERE coin_name = %s ORDER BY timestamp DESC LIMIT %s",
        (coin_name, limit)
    )
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return rows