from flask import Blueprint, jsonify, request

from ..services.order_service import create_order, get_orders


orders_bp = Blueprint("orders", __name__)


@orders_bp.get("/")
def list_orders():
    orders = get_orders()
    result = [
        {
            "id": o.id,
            "client_id": o.client_id,
            "product_id": o.product_id,
            "quantity": o.quantity,
            "total_price": o.total_price,
            "status": o.status,
        }
        for o in orders
    ]
    return jsonify(result)


@orders_bp.post("/")
def add_order():
    data = request.get_json() or {}
    order = create_order(
        data["client_id"],
        data["product_id"],
        data.get("quantity", 1),
    )
    return jsonify({"id": order.id}), 201
