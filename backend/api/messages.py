from flask import Blueprint, jsonify, request

from ..services.messenger_service import get_messages, send_message


messages_bp = Blueprint("messages", __name__)


@messages_bp.get("/")
def list_messages():
    messages = get_messages()
    return jsonify([
        {
            "id": m.id,
            "client_id": m.client_id,
            "supplier_id": m.supplier_id,
            "message": m.message,
            "created_at": m.created_at.isoformat(),
        }
        for m in messages
    ])


@messages_bp.post("/")
def add_message():
    data = request.get_json() or {}
    msg = send_message(
        data.get("message", ""),
        client_id=data.get("client_id"),
        supplier_id=data.get("supplier_id"),
    )
    return jsonify({"id": msg.id}), 201
