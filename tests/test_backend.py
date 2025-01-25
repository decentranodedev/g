"""
Unit and integration tests for the DecentraNode backend API
"""

import unittest
from src.backend.app import app
from src.backend.models import db, Node
from datetime import datetime
import json

class TestBackend(unittest.TestCase):
    """
    Tests for backend API endpoints
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test client and database for the entire test suite.
        """
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.client = app.test_client()

        with app.app_context():
            db.init_app(app)
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the database after all tests.
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_node(self):
        """
        Test the endpoint for creating a new node.
        """
        payload = {
            "operator": "test_operator",
            "resources": 100
        }
        response = self.client.post("/nodes", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Node created successfully", response.get_data(as_text=True))

        # Validate the node in the database
        with app.app_context():
            node = Node.query.first()
            self.assertIsNotNone(node)
            self.assertEqual(node.operator, "test_operator")
            self.assertEqual(node.resources, 100)

    def test_get_nodes(self):
        """
        Test the endpoint for retrieving all nodes.
        """
        # Add a sample node to the database
        with app.app_context():
            new_node = Node(
                operator="test_operator",
                resources=100,
                creation_time=datetime.utcnow(),
                is_active=True
            )
            db.session.add(new_node)
            db.session.commit()

        # Fetch nodes from the API
        response = self.client.get("/nodes")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["operator"], "test_operator")

    def test_update_node(self):
        """
        Test the endpoint for updating node resources.
        """
        # Add a sample node to the database
        with app.app_context():
            new_node = Node(
                operator="test_operator",
                resources=100,
                creation_time=datetime.utcnow(),
                is_active=True
            )
            db.session.add(new_node)
            db.session.commit()
            node_id = new_node.id

        # Update the node
        payload = {"resources": 200}
        response = self.client.put(f"/nodes/{node_id}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Node updated successfully", response.get_data(as_text=True))

        # Validate the update in the database
        with app.app_context():
            node = Node.query.get(node_id)
            self.assertEqual(node.resources, 200)

    def test_deactivate_node(self):
        """
        Test the endpoint for deactivating a node.
        """
        # Add a sample node to the database
        with app.app_context():
            new_node = Node(
                operator="test_operator",
                resources=100,
                creation_time=datetime.utcnow(),
                is_active=True
            )
            db.session.add(new_node)
            db.session.commit()
            node_id = new_node.id

        # Deactivate the node
        response = self.client.post(f"/nodes/{node_id}/deactivate")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Node deactivated successfully", response.get_data(as_text=True))

        # Validate the deactivation in the database
        with app.app_context():
            node = Node.query.get(node_id)
            self.assertFalse(node.is_active)

if __name__ == "__main__":
    unittest.main()
