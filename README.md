# Bunkr Downloader

A simple cli tool to download content from Bunkr.

- Please do not abuse the service.

## Prerequisites

Before running this project, ensure you have the following installed on your system:

- **Python 3.x**
- **Node.js**

<<<<<<< HEAD
To verify your installations:
=======

> > > > > > > a4c9c37 (better mgmt of deps using poetry)

```bash
python3 --version
node --version
```

## Installation & Setup

### 1. Clone the repo

```bash
git clone https://github.com/DebNation/bunkr-downloader
cd bunkr-downloader
```

### 2. Install poetry

```bash
pipx install poetry
```

### 3. install deps

```bash
poetry install bunkr-downloader
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
poetry run bunkr-downloader
```
