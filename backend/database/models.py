from datetime import datetime

from .. import db


class Client(db.Model):
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(50))

    orders = db.relationship("Order", back_populates="client")
    communications = db.relationship("Communication", back_populates="client")


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    contact_info = db.Column(db.String(255))

    products = db.relationship("Product", back_populates="supplier")
    communications = db.relationship("Communication", back_populates="supplier")


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"))

    supplier = db.relationship("Supplier", back_populates="products")
    orders = db.relationship("Order", back_populates="product")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Float)
    status = db.Column(db.String(50))

    client = db.relationship("Client", back_populates="orders")
    product = db.relationship("Product", back_populates="orders")
    documents = db.relationship("Document", back_populates="order")


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    doc_type = db.Column(db.String(50))
    content = db.Column(db.Text)

    order = db.relationship("Order", back_populates="documents")


class Communication(db.Model):
    __tablename__ = "communications"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship("Client", back_populates="communications")
    supplier = db.relationship("Supplier", back_populates="communications")


class ExchangeRate(db.Model):
    __tablename__ = "exchange_rates"

    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), unique=True)
    rate_to_usd = db.Column(db.Float)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


def create_test_data(session):
    """Populate database with sample data if empty."""
    if Client.query.first():
        return

    c1 = Client(name="Alice", email="alice@example.com", phone="123456")
    c2 = Client(name="Bob", email="bob@example.com")
    s1 = Supplier(name="Acme Corp", contact_info="contact@acme.com")
    p1 = Product(name="Widget", price=10.0, supplier=s1)
    o1 = Order(client=c1, product=p1, quantity=2, total_price=20.0, status="new")
    d1 = Document(order=o1, doc_type="invoice", content="Invoice Content")
    m1 = Communication(client=c1, message="Need more widgets")
    r1 = ExchangeRate(currency="EUR", rate_to_usd=1.1)

    session.add_all([c1, c2, s1, p1, o1, d1, m1, r1])
    session.commit()
