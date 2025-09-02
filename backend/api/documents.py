from flask import Blueprint, jsonify

from ..database.models import Document


documents_bp = Blueprint("documents", __name__)


@documents_bp.get("/")
def list_documents():
    documents = Document.query.all()
    return jsonify([
        {
            "id": d.id,
            "order_id": d.order_id,
            "doc_type": d.doc_type,
            "content": d.content,
        }
        for d in documents
    ])
