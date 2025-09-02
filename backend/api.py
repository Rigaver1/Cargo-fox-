from flask import Flask, jsonify
import sqlite3

from .currency_service import (
    DB_PATH,
    get_last_update,
    init_db,
    update_exchange_rates,
)

app = Flask(__name__)


def _current_rates():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        'SELECT target, rate FROM exchange_rates '
        'WHERE fetched_at = (SELECT MAX(fetched_at) FROM exchange_rates)'
    )
    data = cur.fetchall()
    conn.close()
    return dict(data)


@app.route('/api/exchange_rates', methods=['GET'])
def exchange_rates():
    init_db()
    last = get_last_update()
    rates = _current_rates() if last else {}
    return jsonify({
        'rates': rates,
        'last_update': last.isoformat() if last else None,
    })


@app.route('/api/exchange_rates/update', methods=['POST'])
def manual_update():
    ts = update_exchange_rates()
    return jsonify({'updated_at': ts.isoformat()})


if __name__ == '__main__':
    app.run(debug=True)
