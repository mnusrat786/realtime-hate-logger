import csv, os
from datetime import datetime

def save_to_csv(text, hash_val, confidence, true_label):
    log_path = os.path.join(os.getcwd(), "log.csv")
    file_exists = os.path.isfile(log_path)

    with open(log_path, mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Text", "Hash", "Confidence", "True Label"])
        writer.writerow([
            datetime.utcnow().isoformat(),
            text,
            hash_val,
            confidence,
            true_label
        ])
