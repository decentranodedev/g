import React, { useEffect, useState } from "react";
import NodeCard from "../components/NodeCard";

const NodeList = () => {
  const [nodes, setNodes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch nodes from the backend API
    const fetchNodes = async () => {
      try {
        const response = await fetch("/nodes"); // Replace with your backend API URL
        const data = await response.json();
        setNodes(data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching nodes:", error);
        setLoading(false);
      }
    };

    fetchNodes();
  }, []);

  if (loading) {
    return <div className="text-center mt-10">Loading nodes...</div>;
  }

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Node List</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {nodes.length > 0 ? (
          nodes.map((node) => <NodeCard key={node.id} node={node} />)
        ) : (
          <p className="text-gray-600">No nodes available.</p>
        )}
      </div>
    </div>
  );
};

export default NodeList;
