import os
from dotenv import load_dotenv
from web3 import Web3
import json
import solcx

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("GANACHE_RPC")))
private_key = os.getenv("PRIVATE_KEY")
account_address = os.getenv("ACCOUNT_ADDRESS")

# Read and compile contract
with open("contracts/hatelogger.sol", "r") as file:
    contract_source_code = file.read()

solcx.install_solc('0.8.0')
compiled_sol = solcx.compile_source(
    contract_source_code,
    output_values=["abi", "bin"],
    solc_version="0.8.0"
)

contract_id, contract_interface = compiled_sol.popitem()
abi = contract_interface["abi"]
bytecode = contract_interface["bin"]

# Deploy
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(account_address)
txn = contract.constructor().build_transaction({
    "from": account_address,
    "nonce": nonce,
    "gas": 3000000,
    "gasPrice": w3.to_wei("20", "gwei"),
})

signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Contract deployed at address:", tx_receipt.contractAddress)

with open("blockchain/compiled_abi.json", "w") as abi_file:
    json.dump(abi, abi_file)
