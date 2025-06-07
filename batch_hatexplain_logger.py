
import os
import json
import hashlib
from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from web3 import Web3
from dotenv import load_dotenv

# ========== LOAD SECRETS ==========
load_dotenv()

GANACHE_URL = os.getenv("GANACHE_RPC")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")
MODEL_NAME = os.getenv("MODEL_NAME")

# ========== CONFIGURATION ==========
HATEXPLAIN_PATH = "data/HateXplain.json"
MAX_LOGS = 1000
ABI_PATH = "blockchain/compiled_abi.json"

# ========== LOAD MODEL ==========
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# ========== SETUP WEB3 ==========
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))
with open(ABI_PATH) as f:
    abi = json.load(f)

contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

# ========== HELPERS ==========
def compute_sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def detect_hate(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    label = torch.argmax(probs).item()
    confidence = probs[0][label].item()
    return label, confidence

LABEL2ID = {"hatespeech": 0, "offensive": 1, "normal": 2}

# ========== MAIN FUNCTION ==========
def process_hatexplain(path, max_logs):
    with open(path, "r") as f:
        data = json.load(f)

    log_count = 0
    total = 0
    nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)

    print(f"\n Starting batch processing from HateXplain...\n")

    for example in data.values():
        total += 1
        post_tokens = example.get("post_tokens", [])
        text = " ".join(post_tokens)

        predicted_label, confidence = detect_hate(text)

        if predicted_label in [1, 2]:  # offensive or hate
            hash_val = compute_sha256(text)
            labels = [ann['label'] for ann in example['annotators']]
            majority_label = max(set(labels), key=labels.count)
            target = LABEL2ID[majority_label]
            timestamp = datetime.utcnow().isoformat()

            try:
                txn = contract.functions.logHate(
                    hash_val, target, int(confidence * 100), timestamp
                ).build_transaction({
                    'from': ACCOUNT_ADDRESS,
                    'nonce': nonce,
                    'gas': 3000000,
                    'gasPrice': w3.to_wei('20', 'gwei'),
                })

                signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
                tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
                w3.eth.wait_for_transaction_receipt(tx_hash)

                print(f"  Logged #{log_count + 1} | Hash: {hash_val[:10]} | Label: {target} | Confidence: {confidence:.2f}")
                log_count += 1
                nonce += 1  # increment nonce manually for next tx

            except Exception as e:
                print(f"  Failed to log: {e}")

        if log_count >= max_logs:
            break

    print(f"\n Finished. Total Processed: {total} | Hate Logged: {log_count}\n")

# ========== RUN ==========
if __name__ == "__main__":
    process_hatexplain(HATEXPLAIN_PATH, MAX_LOGS)
