"""
Database models for DecentraNode
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class Node(db.Model):
    """
    Node model for storing node-related information.
    """
    __tablename__ = "nodes"

    id = db.Column(db.Integer, primary_key=True)
    operator = db.Column(db.String(100), nullable=False)
    resources = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Node {self.id} - Operator: {self.operator}, Active: {self.is_active}>"

class Transaction(db.Model):
    """
    Transaction model for recording token incentives and payments.
    """
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, db.ForeignKey("nodes.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    # Relationship to the Node model
    node = db.relationship("Node", backref="transactions")

    def __repr__(self):
        return f"<Transaction {self.id} - Node: {self.node_id}, Amount: {self.amount}>"
