from fastapi import FastAPI, HTTPException
from services import get_price
from database import save_price, get_price_history

app = FastAPI()

@app.get("/price/{coin_id}")
def price_endpoint(coin_id: str):
    price = get_price(coin_id)
    
    if price is None:
        raise HTTPException(status_code=404, detail="Coin not found")
    
    # Save to database
    save_price(coin_id, price)
    
    return {
        "coin": coin_id,
        "price_usd": price,
        "saved": True
    }

@app.get("/history/{coin_id}")
def history_endpoint(coin_id: str, limit: int = 10):
    rows = get_price_history(coin_id, limit)
    
    history = []
    for row in rows:
        history.append({
            "coin": row[1],
            "price": row[2],
            "timestamp": row[3].isoformat()
        })
    
    return {"coin": coin_id, "history": history}