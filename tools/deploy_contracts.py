"""
Deployment script for DecentraNode smart contracts
"""

from web3 import Web3
import json
import os

# Configure Web3
INFURA_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"  # Replace with your Infura project ID
PRIVATE_KEY = "YOUR_PRIVATE_KEY"  # Replace with your private key
CONTRACT_OWNER_ADDRESS = "YOUR_WALLET_ADDRESS"  # Replace with your wallet address
GAS_LIMIT = 3000000
GAS_PRICE = Web3.toWei("20", "gwei")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def load_contract(file_path):
    """
    Load the compiled contract from a JSON file.
    :param file_path: Path to the compiled contract file.
    :return: Contract ABI and bytecode.
    """
    with open(file_path, "r") as file:
        contract_json = json.load(file)
        return contract_json["abi"], contract_json["bytecode"]

def deploy_contract(abi, bytecode):
    """
    Deploy a smart contract to the Ethereum blockchain.
    :param abi: Contract ABI.
    :param bytecode: Contract bytecode.
    :return: Deployed contract address.
    """
    try:
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        nonce = w3.eth.getTransactionCount(CONTRACT_OWNER_ADDRESS)
        transaction = contract.constructor().buildTransaction({
            "chainId": 1,  # Mainnet
            "gas": GAS_LIMIT,
            "gasPrice": GAS_PRICE,
            "nonce": nonce,
        })
        signed_tx = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt.contractAddress
    except Exception as e:
        print(f"Error deploying contract: {e}")
        return None

if __name__ == "__main__":
    print("Deploying smart contracts...")
    # Deploy NodeManager.sol
    node_manager_abi, node_manager_bytecode = load_contract(
        "build/contracts/NodeManager.json"
    )
    node_manager_address = deploy_contract(node_manager_abi, node_manager_bytecode)
    if node_manager_address:
        print(f"NodeManager deployed at: {node_manager_address}")
    else:
        print("Failed to deploy NodeManager contract.")

    # Deploy DNDToken.sol
    token_abi, token_bytecode = load_contract("build/contracts/DNDToken.json")
    token_address = deploy_contract(token_abi, token_bytecode)
    if token_address:
        print(f"DNDToken deployed at: {token_address}")
    else:
        print("Failed to deploy DNDToken contract.")
