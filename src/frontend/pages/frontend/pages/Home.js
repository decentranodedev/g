import React from "react";

const Home = () => {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-4xl font-bold text-center mb-4">Welcome to DecentraNode</h1>
      <p className="text-center text-lg text-gray-600">
        DecentraNode simplifies and automates the deployment, monitoring, and optimization of decentralized nodes using AI and blockchain technology.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        <div className="p-6 bg-white shadow-lg rounded-lg">
          <h2 className="text-2xl font-semibold mb-2">Create Nodes</h2>
          <p className="text-gray-700">
            Deploy new nodes seamlessly with optimal resource allocation using our intuitive interface.
          </p>
        </div>
        <div className="p-6 bg-white shadow-lg rounded-lg">
          <h2 className="text-2xl font-semibold mb-2">Monitor Performance</h2>
          <p className="text-gray-700">
            Track node health and performance metrics in real-time with AI-powered analytics.
          </p>
        </div>
        <div className="p-6 bg-white shadow-lg rounded-lg">
          <h2 className="text-2xl font-semibold mb-2">Scale Nodes</h2>
          <p className="text-gray-700">
            Automatically adjust resources based on network demands and performance insights.
          </p>
        </div>
        <div className="p-6 bg-white shadow-lg rounded-lg">
          <h2 className="text-2xl font-semibold mb-2">Earn Rewards</h2>
          <p className="text-gray-700">
            Stake your $DND tokens to secure the network and earn incentives for supporting the ecosystem.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;
