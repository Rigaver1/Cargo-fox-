from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config


db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from .api.orders import orders_bp
    from .api.clients import clients_bp
    from .api.suppliers import suppliers_bp
    from .api.documents import documents_bp
    from .api.messages import messages_bp

    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(clients_bp, url_prefix="/clients")
    app.register_blueprint(suppliers_bp, url_prefix="/suppliers")
    app.register_blueprint(documents_bp, url_prefix="/documents")
    app.register_blueprint(messages_bp, url_prefix="/messages")

    with app.app_context():
        from .database import models  # noqa: WPS433
        db.create_all()
        models.create_test_data(db.session)

    return app
