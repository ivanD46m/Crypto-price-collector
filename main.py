import requests
import psycopg2
from datetime import datetime


def get_price(coin_id):
    url = "https://api.coingecko.com/api/v3/simple/price"

    parameters = {
        "ids": coin_id.lower(),
        "vs_currencies": "usd"
    }
    try: 
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        data = response.json()

        if coin_id in data:
            return data[coin_id]['usd']
        
    except KeyError:
        print("Coin not found! ")

    
try:
    conn = psycopg2.connect(
        dbname = "postgres",
        user = "ivandarlami",
        password = "password",
        host = "localhost"
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS prices(
            id SERIAL PRIMARY KEY,
            coin_name TEXT,
            price FLOAT,
            timestamp TIMESTAMP)            
    """)

    conn.commit()

    coin = "ethereum"
    price = get_price(coin)

    cur.execute(
       "INSERT INTO prices(coin_name, price, timestamp) VALUES (%s, %s, %s)",
        (coin, price, datetime.now())
    )

    conn.commit()
    print("Saved to database!")

    cur.execute("SELECT * FROM prices ORDER BY timestamp DESC LIMIT 5")
    rows = cur.fetchall() 

    for row in rows:
        
        print(f"{row[3]}: {row[1]} is ${row[2]}")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Error: {e}")