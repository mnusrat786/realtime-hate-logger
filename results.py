import pandas as pd
import matplotlib.pyplot as plt

# Load blockchain log data
df = pd.read_csv("blockchain_logs.csv")

# Convert confidence to float if it's not already
df['confidence'] = df['confidence'].astype(float)

# ------- Summary Statistics -------
total_logged = len(df)
avg_confidence = df['confidence'].mean()
label_counts = df['target'].value_counts().sort_index()

# ------- Bar Plot: Label Distribution -------
plt.figure(figsize=(6, 4))
label_counts.plot(kind='bar', color=['red', 'orange', 'green'])
plt.title("Label Distribution in Blockchain Logs")
plt.xlabel("Label (0=Hate, 1=Offensive, 2=Normal)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("label_distribution.png")

# ------- Histogram: Confidence Scores -------
plt.figure(figsize=(6, 4))
plt.hist(df['confidence'], bins=20, color='skyblue', edgecolor='black')
plt.title("Confidence Score Distribution")
plt.xlabel("Confidence")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("confidence_histogram.png")

# ------- Print Stats (Optional) -------
print("Total Logged Samples:", total_logged)
print("Average Confidence:", round(avg_confidence, 4))
print("Label Counts:\n", label_counts)
