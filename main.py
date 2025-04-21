
import csv
import hashlib
from datetime import datetime

from model.detector import detect_hate
from stream.simulator import stream_tweets
from utils.logger_csv import save_to_csv
from utils.hashing import generate_hash as compute_sha256
from blockchain.logger import log_to_blockchain  #  Blockchain logger

TWEET_LIMIT = 30

print("\n Starting real-time hate speech monitor...\n")

total = 0
hate = 0

for text, label in stream_tweets(limit=TWEET_LIMIT):
    total += 1
    print(f" Incoming: {text}\n")

    prediction, confidence = detect_hate(text)

    print(f" Model predicted: {prediction} | Confidence: {confidence:.2f}")

    hash_val = compute_sha256(text)

    if prediction == 1:
        hate += 1
        print(" Hate speech detected! Logging it...")

        # Blockchain logging 
        try:
            log_to_blockchain(
                hash_val=hash_val,
                target=label,
                confidence=confidence,
                timestamp=datetime.now().isoformat()
            )
            print(" Logged to blockchain.\n")
        except Exception as e:
            print(f" Blockchain logging failed: {e}\n")

        # CSV logging 
        save_to_csv(text, hash_val, confidence, label)
    else:
        print(" Clean or uncertain content.\n")

print(f"\n Done. Total Tweets: {total} | Hate Detected: {hate}")
