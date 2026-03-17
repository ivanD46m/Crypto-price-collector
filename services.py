import requests

def get_price(coin_id, currency='usd'):
    url = "https://api.coingecko.com/api/v3/simple/price"

    parameters = {
        "ids": coin_id,
        "vs_currencies": currency
    }

    try:
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        data = response.json()
        if coin_id in data:
            return data[coin_id].get(currency)
    except KeyError:
        return None
    


