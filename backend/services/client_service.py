from .. import db
from ..database.models import Client


def create_client(name: str, email: str, phone: str | None = None) -> Client:
    client = Client(name=name, email=email, phone=phone)
    db.session.add(client)
    db.session.commit()
    return client


def get_clients() -> list[Client]:
    return Client.query.all()
