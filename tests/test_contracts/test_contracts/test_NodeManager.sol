// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../src/contracts/NodeManager.sol";

contract TestNodeManager {
    NodeManager nodeManager;

    function beforeEach() public {
        // Deploy a fresh instance of NodeManager before each test
        nodeManager = new NodeManager(address(this));
    }

    function testCreateNode() public {
        uint256 initialNodeCount = nodeManager.nodeCount();

        // Create a new node
        nodeManager.createNode(100);

        // Check that the node count has increased
        uint256 newNodeCount = nodeManager.nodeCount();
        Assert.equal(newNodeCount, initialNodeCount + 1, "Node count should increase by 1");

        // Validate node details
        (
            address operator,
            uint256 resources,
            uint256 creationTime,
            bool isActive
        ) = nodeManager.nodes(newNodeCount);

        Assert.equal(operator, address(this), "Operator should match the creator");
        Assert.equal(resources, 100, "Resources should be set correctly");
        Assert.isTrue(isActive, "Node should be active");
    }

    function testDeactivateNode() public {
        // Create a new node
        nodeManager.createNode(100);
        uint256 nodeId = nodeManager.nodeCount();

        // Deactivate the node
        nodeManager.deactivateNode(nodeId);

        // Validate node status
        (, , , bool isActive) = nodeManager.nodes(nodeId);
        Assert.isFalse(isActive, "Node should be inactive");
    }

    function testUpdateResources() public {
        // Create a new node
        nodeManager.createNode(100);
        uint256 nodeId = nodeManager.nodeCount();

        // Update the node resources
        nodeManager.updateResources(nodeId, 200);

        // Validate updated resources
        (, uint256 resources, , ) = nodeManager.nodes(nodeId);
        Assert.equal(resources, 200, "Resources should be updated to 200");
    }

    function testTransferIncentive() public {
        // Create a new node
        nodeManager.createNode(100);
        uint256 nodeId = nodeManager.nodeCount();

        // Fund the contract
        payable(address(nodeManager)).transfer(1 ether);

        // Transfer incentive
        nodeManager.transferIncentive(nodeId, 1 ether);

        // Validate the transfer
        Assert.equal(address(this).balance, 1 ether, "Incentive should be transferred to the operator");
    }

    // Fallback function to receive Ether for testing
    receive() external payable {}
}
