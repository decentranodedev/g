"""
Utility functions for the Node Agent
"""

import json
import random

def load_config(config_path):
    """
    Load the configuration file for the agent.
    :param config_path: Path to the configuration file.
    :return: Configuration dictionary.
    """
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        print("Configuration loaded successfully.")
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return {}

def analyze_node_performance(resources):
    """
    Simulate an analysis of node performance.
    :param resources: Resources allocated to the node.
    :return: Dictionary containing performance metrics.
    """
    health = random.randint(50, 100) if resources > 50 else random.randint(20, 70)
    performance = {
        "health": health,
        "resources_used": resources * 0.8,  # Example: 80% of resources are used
        "status": "healthy" if health >= 50 else "critical"
    }
    return performance

def log_event(event_type, message):
    """
    Log an event for debugging or monitoring purposes.
    :param event_type: Type of event (e.g., INFO, WARNING, ERROR).
    :param message: Message to log.
    """
    print(f"[{event_type}] {message}")
