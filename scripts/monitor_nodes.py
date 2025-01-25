"""
Real-Time Node Monitoring Script for DecentraNode
"""

import requests
import time
import logging

# Configure logging
logging.basicConfig(
    filename="node_monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

API_URL = "http://localhost:5000/nodes"  # Replace with your backend API URL
CHECK_INTERVAL = 60  # Time interval in seconds for monitoring nodes


def fetch_nodes():
    """
    Fetch the list of nodes from the API.
    :return: List of nodes or None if an error occurs.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch nodes: {e}")
        return None


def monitor_node_health():
    """
    Monitor the health and performance of nodes and log anomalies.
    """
    logging.info("Starting node monitoring...")

    while True:
        nodes = fetch_nodes()
        if nodes is None:
            logging.warning("No nodes fetched, retrying in the next cycle...")
            time.sleep(CHECK_INTERVAL)
            continue

        for node in nodes:
            node_id = node["id"]
            health = node.get("resources", 0)

            if health < 50:
                logging.warning(
                    f"Node {node_id} is below health threshold. Resources: {health}"
                )
            else:
                logging.info(f"Node {node_id} is healthy. Resources: {health}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        monitor_node_health()
    except KeyboardInterrupt:
        logging.info("Node monitoring stopped by user.")
