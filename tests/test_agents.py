"""
Unit tests for Node Agent functionality
"""

import unittest
from src.agents.node_agent import NodeAgent
from src.agents.utils import load_config

class TestNodeAgent(unittest.TestCase):
    """
    Unit tests for the NodeAgent class
    """
    def setUp(self):
        """
        Set up a test environment for NodeAgent
        """
        config = {
            "agent_name": "TestAgent",
            "default_actions": {
                "deploy_node": {
                    "description": "Deploy a test node",
                },
                "monitor_node": {
                    "description": "Monitor test node health",
                }
            },
        }
        self.agent = NodeAgent(config)

    def test_deploy_node(self):
        """
        Test deploying a new node
        """
        self.agent.deploy_node("node-1", 100)
        self.assertIn("node-1", self.agent.node_status)
        self.assertEqual(self.agent.node_status["node-1"]["resources"], 100)

    def test_monitor_nodes(self):
        """
        Test monitoring node health
        """
        self.agent.deploy_node("node-1", 30)  # Simulate a node with low resources
        self.agent.monitor_nodes()
        self.assertEqual(self.agent.node_status["node-1"]["resources"], 30)

    def test_take_action_scale_up(self):
        """
        Test scaling up a node
        """
        self.agent.deploy_node("node-1", 50)
        self.agent.take_action("node-1", "scale_up")
        self.assertEqual(self.agent.node_status["node-1"]["resources"], 60)

    def test_report_status(self):
        """
        Test generating a node status report
        """
        self.agent.deploy_node("node-1", 50)
        with self.assertLogs() as captured:
            self.agent.report_status()
        self.assertIn("node-1", captured.output[0])

if __name__ == "__main__":
    unittest.main()
