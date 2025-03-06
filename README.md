# AI Data Engineering Assignment

## Overview
This project demonstrates a data engineering pipeline that processes text data using Apache Spark. It downloads the AG News dataset from Hugging Face, performs word frequency analysis, and outputs the results as Parquet files.

## Features
- PySpark-based text processing
- Word frequency analysis (specific words and all words)
- Structured logging system
- Containerized with Docker
- Automated testing with pytest
- CI/CD through GitHub Actions

## Project Structure
```
├── .github/workflows/   # GitHub Actions workflow definitions
├── code/
│   ├── config/          # Configuration files and utilities
│   ├── requirements.txt # Python dependencies
│   ├── script/          # Execution scripts
│   ├── src/             # Source code
│   │   ├── config/      # Configuration handling
│   │   ├── logger/      # Logging utilities
│   │   ├── processing/  # Data processing logic
│   │   ├── spark/       # Spark utilities
│   │   └── main.py      # Main entry point
│   ├── tests/           # Unit tests
│   └── Dockerfile       # Docker container definition
├── logs/                # Output logs directory
└── ztmp/                # Temporary data directory

```
## Setup and Installation
### Local Development
1. Clone the repository
2. Set up a Python virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```
3. Install dependencies
```bash
pip install -r code/requirements.txt
```
4. Run the application
```bash
# Build the Docker image
docker build -t ai-data-engineer-assignment:latest -f code/Dockerfile .

# Run the container
docker run --rm -v $(pwd)/logs:/app/logs -v $(pwd)/ztmp:/app/ztmp ai-data-engineer-assignment:latest
```
## Usage
The application provides two commands:
### Process Specific Words
Counts occurrences of specific words ("president", "the", "Asia") in the dataset:
```bash
python code/src/main.py process_data --cfg code/config/config.yaml -dataset news --dirout output_directory
```
### Process All Words
Counts occurrences of all words in the dataset:
```bash
python code/src/main.py process_data_all --cfg code/config/config.yaml -dataset news --dirout output_directory
```
## CI/CD Pipeline
<img src="./screenshots/workflow_diagram.svg" alt="CI/CD Pipeline" width="50%" />

