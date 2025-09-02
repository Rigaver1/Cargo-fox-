from flask import Blueprint, jsonify, request

from ..services.client_service import create_client, get_clients


clients_bp = Blueprint("clients", __name__)


@clients_bp.get("/")
def list_clients():
    clients = get_clients()
    return jsonify([
        {"id": c.id, "name": c.name, "email": c.email, "phone": c.phone}
        for c in clients
    ])


@clients_bp.post("/")
def add_client():
    data = request.get_json() or {}
    client = create_client(data["name"], data["email"], data.get("phone"))
    return jsonify({"id": client.id}), 201
