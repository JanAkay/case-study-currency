import requests
from datetime import datetime
from extensions import db
from models import ExchangeRate
from app import create_app

app = create_app()

# Your API keys
FIXER_API_KEY = "a40103e9a84d92c8f3a7967cf04517e3"
CURRENCY_LAYER_API_KEY = "202938deaf2aa542e20c389632acc1c8"

# API URLs
SOURCES = {
    "fixer": f"https://data.fixer.io/api/latest?access_key={FIXER_API_KEY}&symbols=USD,EUR,TRY",
    "currencylayer": f"http://api.currencylayer.com/live?access_key={CURRENCY_LAYER_API_KEY}&currencies=TRY,USD,EUR"
}

def fetch_exchange_rates():
    with app.app_context():
        for source, url in SOURCES.items():
            response = requests.get(url)
            data = response.json()

            print(f"\nAPI returns({source}):\n", data)  

            if "error" in data:
                print(f"Error from {source} API: {data['error']}")
                continue  

            #parsing
            if source == "fixer":
                rates = data.get("rates", {})
                try_rate = rates.get("TRY", 1)  # Default  1 
            else:  # currencylayer
                rates = data.get("quotes", {})
                try_rate = rates.get("USDTRY", 1)  # Default 1

            for currency_pair, rate in rates.items():
                print(f" {source} - {currency_pair}: {rate}")  

                # Extract the currency code
                if source == "fixer":
                    if currency_pair == "USD":
                        currency = "USD"
                    elif currency_pair == "EUR":
                        currency = "EUR"
                    elif currency_pair == "TRY":
                        currency = "TRY"
                else:  # currencylayer
                    if currency_pair == "USDTRY":
                        currency = "USD"  
                    elif currency_pair == "USDEUR":
                        currency = "EUR"  
                    else:
                        currency = currency_pair[3:]  

                
                if source == "fixer" and currency == "TRY":
                    buy_price = sell_price = (1/rate)  
                else:
                    if source == "currencylayer" and currency == "USD":
                        buy_price = sell_price = rate  
                    else:
                        buy_price = 1/(rate / try_rate)  
                        sell_price = buy_price  

                
                rate_entry = ExchangeRate(
                    source=source,
                    currency=currency,  
                    rate_date=datetime.utcnow(),
                    buy_price=buy_price,
                    sell_price=sell_price
                )

                db.session.add(rate_entry)

        
        db.session.commit()
        print("Currency fetched and saved to db")

if __name__ == "__main__":
    fetch_exchange_rates()
