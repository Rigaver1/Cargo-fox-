from datetime import datetime

from .. import db
from ..database.models import ExchangeRate


def get_rate(currency: str) -> ExchangeRate | None:
    return ExchangeRate.query.filter_by(currency=currency.upper()).first()


def update_rate(currency: str, rate_to_usd: float) -> ExchangeRate:
    rate = ExchangeRate.query.filter_by(currency=currency.upper()).first()
    if rate is None:
        rate = ExchangeRate(currency=currency.upper(), rate_to_usd=rate_to_usd)
        db.session.add(rate)
    else:
        rate.rate_to_usd = rate_to_usd
        rate.updated_at = datetime.utcnow()
    db.session.commit()
    return rate
