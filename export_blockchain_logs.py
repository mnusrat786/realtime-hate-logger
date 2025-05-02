
import os
from dotenv import load_dotenv
from web3 import Web3
import json
import pandas as pd

load_dotenv()

# --- Configuration ---
GANACHE_URL = os.getenv("GANACHE_RPC")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
ABI_PATH = "blockchain/compiled_abi.json"

# --- Setup web3 ---
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
with open(ABI_PATH) as f:
    abi = json.load(f)

contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

# --- Read logs from smart contract ---
logs = contract.functions.getLogs().call()

# --- Save to CSV ---
df = pd.DataFrame(logs, columns=["hash", "target", "confidence", "timestamp"])
df.to_csv("blockchain_logs.csv", index=False)
print("Exported blockchain logs to blockchain_logs.csv")
