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

            # Parsing for rates
            if source == "fixer":
                rates = data.get("rates", {})
                try_rate = rates.get("TRY", 1)  # Default to 1 if TRY is not found (but it should be in fixer)
            else:  # currencylayer
                rates = data.get("quotes", {})
                try_rate = rates.get("USDTRY", 1)  # Default to 1 if USDTRY is not found

            for currency_pair, rate in rates.items():
                print(f"💰 {source} - {currency_pair}: {rate}")  

                # Extract the currency code from the pair (USDTRY → TRY, USDEUR → EUR)
                if currency_pair == "USDTRY":
                    currency = "TRY"
                elif currency_pair == "USDEUR":
                    currency = "EUR"
                else:
                    currency = currency_pair[3:]  # For other cases like USD, EUR, we use the last part of the pair

                # Convert all rates to TRY by dividing with TRY rate
                if currency == "TRY":
                    buy_price = sell_price = rate  # Already in TRY
                else:
                    buy_price = rate / try_rate  # Convert to TRY by dividing with USDTRY
                    sell_price = buy_price  # For simplicity, assume buy and sell price are the same

                # Add entry to database
                rate_entry = ExchangeRate(
                    source=source,
                    currency=currency,  
                    rate_date=datetime.utcnow(),
                    buy_price=buy_price,
                    sell_price=sell_price
                )

                db.session.add(rate_entry)

        # Commit the changes to the database
        db.session.commit()
        print("✅ Currency rates fetched and saved to the database.")

if __name__ == "__main__":
    fetch_exchange_rates()
