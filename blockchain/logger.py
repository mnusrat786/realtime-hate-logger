import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Connect to local Ganache
w3 = Web3(Web3.HTTPProvider(os.getenv("GANACHE_RPC")))
assert w3.is_connected(), "Web3 is not connected to Ganache"

# Load ABI
with open("blockchain/compiled_abi.json", "r") as f:
    contract_abi = json.load(f)

# Get contract address from env
contract_address = os.getenv("CONTRACT_ADDRESS")

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Wallet setup
private_key = os.getenv("PRIVATE_KEY")
account_address = os.getenv("ACCOUNT_ADDRESS")

def log_to_blockchain(hash_val, confidence, target, timestamp):
    try:
        nonce = w3.eth.get_transaction_count(account_address)

        txn = contract.functions.logHate(
            hash_val,
            target,
            int(confidence * 100),
            timestamp
        ).build_transaction({
            'from': account_address,
            'gas': 3000000,
            'gasPrice': w3.to_wei('20', 'gwei'),
            'nonce': nonce
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"[BLOCKCHAIN] Logged hash: {hash_val}")
    except Exception as e:
        print(f"Blockchain logging failed: {e}")
