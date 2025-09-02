from flask import Blueprint, jsonify, request

from ..services.supplier_service import create_supplier, get_suppliers


suppliers_bp = Blueprint("suppliers", __name__)


@suppliers_bp.get("/")
def list_suppliers():
    suppliers = get_suppliers()
    return jsonify([
        {"id": s.id, "name": s.name, "contact_info": s.contact_info}
        for s in suppliers
    ])


@suppliers_bp.post("/")
def add_supplier():
    data = request.get_json() or {}
    supplier = create_supplier(data["name"], data.get("contact_info"))
    return jsonify({"id": supplier.id}), 201
