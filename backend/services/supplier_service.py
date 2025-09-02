from .. import db
from ..database.models import Supplier


def create_supplier(name: str, contact_info: str | None = None) -> Supplier:
    supplier = Supplier(name=name, contact_info=contact_info)
    db.session.add(supplier)
    db.session.commit()
    return supplier


def get_suppliers() -> list[Supplier]:
    return Supplier.query.all()
