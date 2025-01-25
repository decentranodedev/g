// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract NodeManager {
    // State variables
    address public owner;
    IERC20 public dndToken; // $DND token for incentives
    uint256 public nodeCount;

    struct Node {
        address operator;
        uint256 resources;
        uint256 creationTime;
        bool isActive;
    }

    mapping(uint256 => Node) public nodes;

    // Events
    event NodeCreated(uint256 indexed nodeId, address indexed operator, uint256 resources);
    event NodeDeactivated(uint256 indexed nodeId);
    event ResourcesUpdated(uint256 indexed nodeId, uint256 newResources);

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    modifier nodeExists(uint256 nodeId) {
        require(nodes[nodeId].operator != address(0), "Node does not exist");
        _;
    }

    // Constructor
    constructor(address _dndToken) {
        owner = msg.sender;
        dndToken = IERC20(_dndToken);
    }

    // Functions
    function createNode(uint256 resources) external {
        require(resources > 0, "Resources must be greater than zero");

        nodeCount++;
        nodes[nodeCount] = Node({
            operator: msg.sender,
            resources: resources,
            creationTime: block.timestamp,
            isActive: true
        });

        emit NodeCreated(nodeCount, msg.sender, resources);
    }

    function deactivateNode(uint256 nodeId) external onlyOwner nodeExists(nodeId) {
        nodes[nodeId].isActive = false;
        emit NodeDeactivated(nodeId);
    }

    function updateResources(uint256 nodeId, uint256 newResources) external nodeExists(nodeId) {
        require(msg.sender == nodes[nodeId].operator, "Not the node operator");
        require(newResources > 0, "Resources must be greater than zero");

        nodes[nodeId].resources = newResources;
        emit ResourcesUpdated(nodeId, newResources);
    }

    function getNodeDetails(uint256 nodeId) external view nodeExists(nodeId) returns (Node memory) {
        return nodes[nodeId];
    }

    function transferIncentive(uint256 nodeId, uint256 amount) external nodeExists(nodeId) onlyOwner {
        require(nodes[nodeId].isActive, "Node is not active");
        require(dndToken.balanceOf(address(this)) >= amount, "Insufficient DND balance");

        dndToken.transfer(nodes[nodeId].operator, amount);
    }
}
