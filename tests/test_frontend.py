"""
End-to-end tests for DecentraNode's frontend
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import time

class TestFrontend(unittest.TestCase):
    """
    Test suite for frontend functionality using Selenium
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the Selenium WebDriver for the test suite
        """
        cls.driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and available
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://localhost:3000"  # Replace with your frontend URL

    @classmethod
    def tearDownClass(cls):
        """
        Close the WebDriver after all tests
        """
        cls.driver.quit()

    def test_home_page_loads(self):
        """
        Test that the home page loads successfully
        """
        self.driver.get(self.base_url)
        title = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(title, "Welcome to DecentraNode", "Home page title does not match")

    def test_node_list_page(self):
        """
        Test that the Node List page loads and displays nodes
        """
        self.driver.get(f"{self.base_url}/nodes")
        heading = self.driver.find_element(By.TAG_NAME, "h1").text
        self.assertEqual(heading, "Node List", "Node List page title does not match")

        # Wait for nodes to load
        time.sleep(2)
        nodes = self.driver.find_elements(By.CLASS_NAME, "card")
        self.assertGreater(len(nodes), 0, "No nodes found on the Node List page")

    def test_create_node(self):
        """
        Test the Create Node functionality
        """
        self.driver.get(f"{self.base_url}/nodes/create")
        operator_input = self.driver.find_element(By.NAME, "operator")
        resources_input = self.driver.find_element(By.NAME, "resources")
        submit_button = self.driver.find_element(By.TAG_NAME, "button")

        # Fill out the form
        operator_input.send_keys("Test Operator")
        resources_input.send_keys("100")
        submit_button.click()

        # Verify success message
        time.sleep(2)
        success_message = self.driver.find_element(By.CLASS_NAME, "success").text
        self.assertIn("Node created successfully", success_message, "Node creation failed")

if __name__ == "__main__":
    unittest.main()
