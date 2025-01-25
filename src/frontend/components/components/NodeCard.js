import React from "react";

const NodeCard = ({ node }) => {
  return (
    <div className="p-4 bg-white shadow-md rounded-lg border border-gray-200">
      <h3 className="text-xl font-bold mb-2">Node ID: {node.id}</h3>
      <p className="text-gray-600">Operator: {node.operator}</p>
      <p className="text-gray-600">Resources: {node.resources}</p>
      <p className="text-gray-600">Status: {node.is_active ? "Active" : "Inactive"}</p>
      <p className="text-gray-600">
        Created On: {new Date(node.creation_time).toLocaleDateString()}
      </p>
      <button
        className={`mt-4 px-4 py-2 ${
          node.is_active
            ? "bg-red-500 hover:bg-red-600"
            : "bg-green-500 hover:bg-green-600"
        } text-white font-semibold rounded-lg`}
      >
        {node.is_active ? "Deactivate" : "Activate"}
      </button>
    </div>
  );
};

export default NodeCard;
