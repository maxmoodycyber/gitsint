# GitSint - GitHub Email Intelligence Tool

GitSint is a Python-based tool designed to extract email addresses from GitHub user commits. It specifically focuses on finding real email addresses associated with a GitHub user by analyzing their commit history.

## Features

- 🔍 Scans non-fork repositories only
- 📧 Extracts real email addresses from commit patches
- 🔗 Provides commit URLs where emails were found
- ⚡ Uses concurrent processing for faster scanning
- 🚫 Automatically filters out GitHub's no-reply emails
- 📝 Saves results in real-time to results.txt
- ⏱️ Respects GitHub API rate limits

## Installation

1. Clone the repository:
```bash
git clone https://github.com/maxmoodycyber/gitsint.git
cd gitsint
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script with:
```bash
python gitsint.py
```

When prompted, enter the GitHub user URL you want to scan (e.g., `https://github.com/maxmoodycyber`).

The script will:
1. Scan all non-fork repositories owned by the user
2. Check commits made by the user
3. Extract email addresses from commit patches
4. Save results to `results.txt` in real-time
5. Display progress in the terminal

## Output Format

Results are saved in `results.txt` with the following format:
```
Email scan results for GitHub user: username
==================================================

Email: example@email.com
Found in: https://github.com/username/repo/commit/123abc.patch

Email: another@email.com
Found in: https://github.com/username/repo/commit/456def.patch
```

## Requirements

- Python 3.6+
- requests library

## Notes

- The tool only scans commits made by the specified user
- Forks are automatically excluded from the scan
- GitHub's no-reply email addresses are filtered out
- Results are saved in real-time as they're found
- The script includes a 1-second delay between repository scans to respect GitHub's API rate limits

## Disclaimer

This tool is intended for legitimate purposes only. Please respect GitHub's Terms of Service and use this tool responsibly. 