from .. import db
from ..database.models import Communication


def send_message(message: str, client_id: int | None = None, supplier_id: int | None = None) -> Communication:
    comm = Communication(client_id=client_id, supplier_id=supplier_id, message=message)
    db.session.add(comm)
    db.session.commit()
    return comm


def get_messages() -> list[Communication]:
    return Communication.query.order_by(Communication.created_at.desc()).all()
