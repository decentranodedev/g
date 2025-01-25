"""
API routes for DecentraNode
"""

from flask import Blueprint, jsonify, request
from models import db, Node, Transaction
from datetime import datetime

# Define the blueprint for routes
routes = Blueprint("routes", __name__)

def register_routes(app):
    """
    Register all routes with the Flask app.
    """
    app.register_blueprint(routes)

# Node routes
@routes.route("/nodes", methods=["GET"])
def get_nodes():
    """
    Retrieve all nodes.
    """
    nodes = Node.query.all()
    result = [
        {
            "id": node.id,
            "operator": node.operator,
            "resources": node.resources,
            "creation_time": node.creation_time,
            "is_active": node.is_active,
        }
        for node in nodes
    ]
    return jsonify(result), 200

@routes.route("/nodes", methods=["POST"])
def create_node():
    """
    Create a new node.
    """
    data = request.json
    new_node = Node(
        operator=data.get("operator"),
        resources=data.get("resources"),
        creation_time=datetime.utcnow(),
        is_active=True,
    )
    db.session.add(new_node)
    db.session.commit()
    return jsonify({"message": "Node created successfully", "node_id": new_node.id}), 201

@routes.route("/nodes/<int:node_id>", methods=["PUT"])
def update_node(node_id):
    """
    Update resources for a specific node.
    """
    node = Node.query.get(node_id)
    if not node:
        return jsonify({"error": "Node not found"}), 404

    data = request.json
    node.resources = data.get("resources", node.resources)
    db.session.commit()
    return jsonify({"message": "Node updated successfully"}), 200

@routes.route("/nodes/<int:node_id>/deactivate", methods=["POST"])
def deactivate_node(node_id):
    """
    Deactivate a specific node.
    """
    node = Node.query.get(node_id)
    if not node:
        return jsonify({"error": "Node not found"}), 404

    node.is_active = False
    db.session.commit()
    return jsonify({"message": "Node deactivated successfully"}), 200

# Transaction routes
@routes.route("/transactions", methods=["POST"])
def create_transaction():
    """
    Create a new transaction for a node.
    """
    data = request.json
    node_id = data.get("node_id")
    amount = data.get("amount")

    node = Node.query.get(node_id)
    if not node:
        return jsonify({"error": "Node not found"}), 404

    transaction = Transaction(
        node_id=node_id,
        amount=amount,
        timestamp=datetime.utcnow(),
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction recorded successfully"}), 201

@routes.route("/transactions/<int:node_id>", methods=["GET"])
def get_transactions(node_id):
    """
    Retrieve transactions for a specific node.
    """
    node = Node.query.get(node_id)
    if not node:
        return jsonify({"error": "Node not found"}), 404

    transactions = Transaction.query.filter_by(node_id=node_id).all()
    result = [
        {"id": txn.id, "amount": txn.amount, "timestamp": txn.timestamp}
        for txn in transactions
    ]
    return jsonify(result), 200
