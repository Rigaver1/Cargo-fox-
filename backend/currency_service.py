import argparse
import datetime as dt
import sqlite3
import time
from typing import Dict, Tuple

import requests
import schedule

DB_PATH = 'exchange_rates.db'


def init_db() -> None:
    """Create the exchange_rates table if it does not already exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS exchange_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base TEXT NOT NULL,
            target TEXT NOT NULL,
            rate REAL NOT NULL,
            source TEXT NOT NULL,
            fetched_at TIMESTAMP NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def _fetch_from_cbr() -> Tuple[Dict[str, float], str]:
    """Fetch rates from the Central Bank of Russia."""
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()['Valute']
    rates = {code: info['Value'] for code, info in data.items()}
    return rates, 'cbr'


def _fetch_from_fallback() -> Tuple[Dict[str, float], str]:
    """Fallback source for exchange rates."""
    url = 'https://api.exchangerate.host/latest?base=RUB'
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json()['rates']
    return data, 'exchangerate.host'


def get_exchange_rates() -> Tuple[Dict[str, float], str]:
    """Attempt to fetch rates from CBR, falling back to a secondary source."""
    try:
        return _fetch_from_cbr()
    except Exception:
        try:
            return _fetch_from_fallback()
        except Exception as exc:  # pragma: no cover - simple error propagation
            raise RuntimeError('Failed to fetch exchange rates') from exc


def save_rates(rates: Dict[str, float], source: str) -> dt.datetime:
    """Persist rates to the database and return the timestamp used."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now = dt.datetime.utcnow()
    for target, rate in rates.items():
        cur.execute(
            'INSERT INTO exchange_rates (base, target, rate, source, fetched_at) '
            'VALUES (?, ?, ?, ?, ?)',
            ('RUB', target, rate, source, now),
        )
    conn.commit()
    conn.close()
    return now


def update_exchange_rates() -> dt.datetime:
    """Fetch latest rates and store them in the database."""
    rates, source = get_exchange_rates()
    return save_rates(rates, source)


def get_last_update() -> dt.datetime | None:
    """Return timestamp of the most recent exchange rates update."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT MAX(fetched_at) FROM exchange_rates')
    row = cur.fetchone()
    conn.close()
    if row and row[0]:
        return dt.datetime.fromisoformat(row[0])
    return None


def schedule_updates() -> None:
    """Run an update job every 24 hours."""
    schedule.every(24).hours.do(update_exchange_rates)
    while True:  # pragma: no cover - long running loop
        schedule.run_pending()
        time.sleep(60)


def main() -> None:
    parser = argparse.ArgumentParser(description='Exchange rate updater')
    parser.add_argument(
        '--update', action='store_true', help='Run a single manual update and exit'
    )
    parser.add_argument(
        '--schedule', action='store_true', help='Run a scheduler that updates every 24h'
    )
    args = parser.parse_args()

    init_db()
    if args.update:
        ts = update_exchange_rates()
        print(f'Updated at {ts.isoformat()}')
    elif args.schedule:
        schedule_updates()
    else:
        rates, source = get_exchange_rates()
        print(f'Fetched {len(rates)} rates from {source}')


if __name__ == '__main__':
    main()
