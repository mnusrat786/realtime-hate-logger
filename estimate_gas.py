import os
from dotenv import load_dotenv
from web3 import Web3
import json
from datetime import datetime

load_dotenv()

# --- Configuration ---
GANACHE_URL = os.getenv("GANACHE_RPC")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
ABI_PATH = "blockchain/compiled_abi.json"

# --- Connect to Ganache ---
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
account = w3.eth.accounts[0]

# --- Load ABI ---
with open(ABI_PATH, "r") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

# --- Dummy Values for Estimation ---
dummy_hash = "a" * 64  # Fake 64-character SHA-256 hash
dummy_target = 0        # Hate
dummy_conf = 85         # 85% confidence
dummy_time = datetime.utcnow().isoformat()

# --- Estimate Gas ---
estimated_gas = contract.functions.logHate(
    dummy_hash,
    dummy_target,
    dummy_conf,
    dummy_time
).estimate_gas({'from': account})

# --- Cost Estimation ---
gas_price = w3.to_wei('10', 'gwei')  # Set test gas price
total_cost_wei = estimated_gas * gas_price
total_cost_eth = w3.from_wei(total_cost_wei, 'ether')

print(f"Estimated Gas: {estimated_gas} units")
print(f"Gas Price: {gas_price} wei")
print(f"Total Cost: {total_cost_wei} wei (~{total_cost_eth:.8f} ETH)")
