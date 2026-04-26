# CryptoTerminal Pro: A Scientific Data Pipeline

## Overview
This project implements a robust Data Pipeline (ETL) and Command Line Interface (CLI) designed for the acquisition, processing, and analysis of cryptocurrency market data. The core objective is to demonstrate a clean software architecture applied to scientific data management, ensuring data integrity, idempotency, and efficient storage.

## Architecture & Design Patterns
The system follows the **Model-View-Controller (MVC)** architectural pattern, ensuring a strict separation of concerns:

- **Models:** Built with Python `dataclasses` for type-safe data handling.
- **Services (Logic Layer):** - `api_client.py`: Handles network I/O with an exponential backoff retry mechanism.
  - `processor.py`: Utilizes **Pandas** for time-series normalization and data cleaning.
- **Views:** Console rendering via the `rich` library.
- **Controllers:** Orchestrates the flow between the network layer and local persistence.

## 🛠️ Key Technical Features

### Data Processing and Storage
- **Pandas Integration:** Used for normalizing heterogeneous data from the CoinGecko API and converting time-series timestamps.
- **Parquet Format:** Data is stored in **Apache Parquet**, a columnar storage format optimized for scientific computation and heavy data loads, offering better performance and compression than CSV or JSON.
- **Data Integrity:** The pipeline implements an idempotent "Append and Save" logic, automatically removing duplicate records based on unique timestamps and coin IDs.

### Robust Testing
The project includes a comprehensive suite of unit tests using **PyTest**. It utilizes `tmp_path` fixtures to simulate file system operations in isolated environments, ensuring the processing logic remains bulletproof without affecting real production data.

## Project Structure & `__init__.py` Note
```text
src/
├── controllers/
├── models/
├── services/
├── views/
├── main.py
tests/
```

### Why use empty `__init__.py` files?
Every subdirectory in `src/` and the `tests/` folder contains an `__init__.py` file. While modern Python supports implicit namespace packages, these files are intentionally included for two reasons:

1. **Explicit Package Declaration:** They explicitly mark directories as Python packages, ensuring that absolute imports (e.g., `from src.models...`) work consistently across different environments and IDEs.
2. **Test Discovery:** They facilitate **PyTest** in correctly discovering modules and managing the `PYTHONPATH` during automated testing cycles, preventing common `ModuleNotFoundError` issues.

## Getting Started

### Installation
1. Clone the repository and navigate to the project root.
2. Create a virtual environment: `python -m venv venv`.
3. Install dependencies: `pip install -r requirements.txt`.

### Usage
**Interactive Mode:**
```bash
python src/main.py
```

**CLI Mode (Automation):**
- Fetch live data: `python src/main.py --action fetch --coin bitcoin --currency usd`
- Download history: `python src/main.py --action history --coin ethereum --days 30`
- Analyze local DB: `python src/main.py --action analyze --coin bitcoin`

### Running Tests
Execute the following command to run the test suite:
```bash
pytest
```



