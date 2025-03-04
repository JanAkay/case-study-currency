from flask import Blueprint, jsonify, request
from extensions import db
from models import ExchangeRate

bp = Blueprint("api", __name__)

# last currency info
@bp.route("/rates/<currency>", methods=["GET"])
def get_latest_rate(currency):
    rate = ExchangeRate.query.filter_by(currency=currency).order_by(ExchangeRate.rate_date.desc()).first()
    if not rate:
        return jsonify({"error": "Currency info not found"}), 404

    return jsonify({
        "currency": rate.currency,
        "source": rate.source,
        "rate_date": rate.rate_date,
        "buy_price": rate.buy_price,
        "sell_price": rate.sell_price
    })

# filtered currency info
@bp.route("/rates", methods=["GET"])
def get_filtered_rates():
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 10))
    rate_source = request.args.get("rateSource")
    currency = request.args.get("currency")

    print(f" Filter Parameters - Page: {page}, Size: {size}, Rate Source: {rate_source}, Currency: {currency}")

    query = ExchangeRate.query
    if rate_source:
        query = query.filter_by(source=rate_source)
    if currency:
        query = query.filter_by(currency=currency)

    rates = query.order_by(ExchangeRate.rate_date.desc()).paginate(page=page, per_page=size, error_out=False)

    print(f"🔍 Number of entries in db: {rates.total}")

    if rates.total == 0:
        return jsonify({"error": "No data found"}), 404

    return jsonify({
        "total": rates.total,
        "pages": rates.pages,
        "current_page": page,
        "rates": [{
            "currency": rate.currency,
            "source": rate.source,
            "rate_date": rate.rate_date,
            "buy_price": rate.buy_price,
            "sell_price": rate.sell_price
        } for rate in rates.items]
    })

