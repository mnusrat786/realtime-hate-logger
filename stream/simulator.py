from datasets import load_dataset
from collections import Counter
import time
import random
def stream_tweets(limit=30):  #  Add this argument
    dataset = load_dataset("hatexplain", trust_remote_code=True)["train"]
    for i, tweet in enumerate(dataset):
        if i >= limit:
            break
        text = " ".join(tweet["post_tokens"])
        label_votes = tweet["annotators"]["label"]
        label = Counter(label_votes).most_common(1)[0][0]
        yield text, label
        time.sleep(random.uniform(1.5, 3.0))  # simulate real-time stream
