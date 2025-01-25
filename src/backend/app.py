"""
Backend API for DecentraNode Platform
"""

from flask import Flask, jsonify, request
from models import Node, db
from routes import register_routes

# Initialize the Flask app
app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///decentranode.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

@app.before_first_request
def create_tables():
    """
    Create database tables before the first request.
    """
    db.create_all()

# Register routes
register_routes(app)

@app.route("/")
def home():
    """
    Root endpoint for health check.
    """
    return jsonify({"message": "Welcome to DecentraNode API"}), 200

# Error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
