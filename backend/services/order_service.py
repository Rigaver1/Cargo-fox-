from .. import db
from ..database.models import Client, Order, Product


def create_order(client_id: int, product_id: int, quantity: int) -> Order:
    client = Client.query.get(client_id)
    product = Product.query.get(product_id)
    if client is None or product is None:
        raise ValueError("Invalid client or product")
    order = Order(
        client=client,
        product=product,
        quantity=quantity,
        total_price=product.price * quantity,
        status="new",
    )
    db.session.add(order)
    db.session.commit()
    return order


def get_orders() -> list[Order]:
    return Order.query.all()
