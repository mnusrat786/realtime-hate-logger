
# Blockchain Hate Logger

Blockchain Hate Logger is a real-time simulation system that detects hate speech in tweets using a transformer-based model (DeHateBERT) and logs flagged content immutably on the Ethereum blockchain using smart contracts and SHA-256 hashing.

This project demonstrates how AI and blockchain can be integrated to enable tamper-proof, privacy-preserving, and verifiable content moderation.

---

## Features

- Real-time hate speech detection using DeHateBERT
- SHA-256 hashing for privacy-preserving logging
- Ethereum smart contract integration using Web3.py
- Immutable logging on local blockchain (Ganache)
- Real-time and batch processing modes
- CSV export of blockchain logs
- Transparent, auditable, and research-oriented design

---

## Tech Stack

- **Model**: `Hate-speech-CNERG/dehatebert-mono-english`
- **Blockchain**: Ethereum smart contracts via Ganache
- **Libraries**: HuggingFace Transformers, Web3.py, python-dotenv, torch
- **Dataset**: [HateXplain](https://arxiv.org/abs/2012.10289)

---

## Requirements

- Python 3.10+
- Ganache (GUI or CLI)
- Install dependencies:

```bash
pip install -r requirements.txt
```
### .env Setup  
Create a `.env` file in the project root directory:
```bash
GANACHE_RPC=http://127.0.0.1:7545
PRIVATE_KEY=your_ganache_private_key
ACCOUNT_ADDRESS=your_ganache_account_address
CONTRACT_ADDRESS=your_deployed_contract_address
MODEL_NAME=Hate-speech-CNERG/dehatebert-mono-english
```
### Usage

**1. Real-Time Simulation**  
Simulates streaming 30 tweets and logs hate/offensive content:

```bash
python main.py
```
**2. Batch Logger**
Processes the HateXplain dataset and logs the top 1,000 most confident hate/offensive tweets: 
```bash
python batch_logger.py
```
**3. Export Blockchain Logs to CSV**
Exports all blockchain-logged entries into a CSV file:
```bash
python export_blockchain_logs.py
```

### Folder Structure

```text
realtime-hate-logger/
├── blockchain/                 # Web3 logging (compiled ABI, logger)
│   ├── compiled_abi.json
│   └── logger.py
│
├── contracts/                  # Solidity smart contract
│   └── hatelogger.sol
│
├── dashboard/                  # Streamlit dashboard (optional)
│   └── streamlit_app.py
│
├── data/                       # HateXplain dataset
│   └── HateXplain.json
│
├── model/                      # DeHateBERT model wrapper
│   └── detector.py
│
├── stream/                     # Tweet stream simulation
│   └── simulator.py
│
├── utils/                      # Utility scripts (hashing, CSV logging)
│   ├── hashing.py
│   └── logger_csv.py
│
├── .env                        # Environment variables (ignored)
├── .env.example                # Sample env structure
├── .gitignore
├── README.md
├── requirements.txt
│
├── analysis.ipynb              # Optional: Jupyter analysis
├── batch_hatexplain_logger.py  # Batch logging for 1000 tweets
├── deploy_contract.py          # Deploy smart contract to Ganache
├── download_hatexplain.py      # Download and prepare HateXplain
├── estimate_gas.py             # Estimate gas cost per transaction
├── export_blockchain_logs.py   # Export logs from contract to CSV
├── results.py                  # Summarized result analysis
│
├── blockchain_logs.csv         # Exported logs
├── log.csv                     # Local CSV log
│
├── confidence_histogram.png    # Visualization
├── label_distribution.png      # Visualization
└── logs_over_time.png          # Visualization
```

### Output Example

```bash
Model predicted: 1 | Confidence: 0.82
Hate speech detected! Logging it...
[BLOCKCHAIN] Logged hash: 2e603d4b38...
```
### License
MIT License — use, share, or modify with attribution.

### Author
Muhammad Osama Nusrat
MS Artificial Intelligence
FAST NUCES, Islamabad
Email: osamanusrat786@gmail.com

## Acknowledgements

- [HateXplain Dataset](https://arxiv.org/abs/2012.10289)
- [DeHateBERT Model](https://huggingface.co/Hate-speech-CNERG/dehatebert-mono-english)
- [Web3.py](https://web3py.readthedocs.io/)
- [Ganache](https://trufflesuite.com/ganache/)


