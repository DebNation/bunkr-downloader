# Bunkr Downloader

A Python-based downloader tool for processing URLs from bunkr.

## Prerequisites

Before running this project, ensure you have the following installed on your system:

- **Python 3.x**
- **Node.js** 

To verify your installations:
```bash
python3 --version
node --version
```

## Installation & Setup

### 1. Clone or Download the Project
```bash
git clone https://github.com/DebNation/bunkr-downloader
cd bunkr-downloader
```

### 2. Create Virtual Environment
```bash
python3 -m venv bunkr-downloader-env
```

### 3. Activate Virtual Environment

**For Linux/macOS:**
```bash
source bunkr-downloader-env/bin/activate
```

**For Windows (Command Prompt):**
```cmd
bunkr-downloader-env\Scripts\activate.bat
```

**For Windows (PowerShell):**
```powershell
bunkr-downloader-env\Scripts\Activate.ps1
```

**For Windows (Git Bash):**
```bash
source bunkr-downloader-env/Scripts/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### 1. Add URLs
Paste your URLs in the `URLS.txt` file, one URL per line:
```
https://example1.com
https://example2.com
https://example3.com
```

### 2. Run the Downloader
```bash
python main.py
```

## Deactivating Virtual Environment

When you're done using the tool, deactivate the virtual environment:
```bash
deactivate
```
