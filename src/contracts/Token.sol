// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DNDToken is ERC20 {
    // Address of the contract owner
    address public owner;

    // Modifier to restrict functions to only the owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    // Constructor
    constructor(uint256 initialSupply) ERC20("DecentraNode Token", "DND") {
        owner = msg.sender;
        _mint(msg.sender, initialSupply * (10 ** decimals()));
    }

    // Function to mint additional tokens (restricted to owner)
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    // Function to burn tokens from an account
    function burn(uint256 amount) external {
        _burn(msg.sender, amount);
    }

    // Function to transfer ownership of the token contract
    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Invalid address");
        owner = newOwner;
    }
}
