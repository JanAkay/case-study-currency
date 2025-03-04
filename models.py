from extensions import db
from datetime import datetime

class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)  
    currency = db.Column(db.String(10), nullable=False)  
    rate_date = db.Column(db.DateTime, nullable=False)  
    buy_price = db.Column(db.Float, nullable=False)  
    sell_price = db.Column(db.Float, nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  

    def __repr__(self):
        return f"<ExchangeRate {self.currency} - {self.rate_date}>"
