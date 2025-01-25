import { useState, useEffect } from "react";

/**
 * Custom React hook for fetching and managing nodes.
 * @returns {Object} { nodes, loading, error }
 */
const useNodes = () => {
  const [nodes, setNodes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch nodes from the backend API
    const fetchNodes = async () => {
      try {
        const response = await fetch("/nodes"); // Replace with your backend API endpoint
        if (!response.ok) {
          throw new Error("Failed to fetch nodes");
        }
        const data = await response.json();
        setNodes(data);
      } catch (err) {
        console.error("Error fetching nodes:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchNodes();
  }, []);

  return { nodes, loading, error };
};

export default useNodes;
