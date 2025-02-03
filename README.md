# Web Scraping Script Using Selenium

## Description
This script automates the process of logging into a website and extracting client data using Selenium in Python. The extracted data is saved into an Excel file (`data.xlsx`).

## Requirements

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Google Chrome browser
- ChromeDriver (managed automatically by `webdriver-manager`)

### Required Python Packages
The script relies on the following Python libraries:
- `selenium`
- `webdriver-manager`
- `pandas`
- `openpyxl`

Install all dependencies using:
```sh
pip install selenium webdriver-manager pandas openpyxl
```

## How to Run the Script

### 1. Clone or Download the Repository
Download the script and navigate to the directory in your terminal.

### 2. Update Credentials
Modify the `username` and `password` variables in the script:
```python
username = 'your_username'
password = 'your_password'
```

### 3. Run the Script
Execute the script using:
```sh
python script.py
```

### 4. Output
The extracted data will be saved in `data.xlsx` in the same directory.

## Notes
- The script will iterate through client IDs from `1` to `5000`. You may need to adjust this range based on your requirements.
- If the script encounters an error, it will print an error message and continue.
- Ensure that the website URL and element identifiers (IDs, XPaths) are correct.

## Troubleshooting
- If the script fails to run, ensure you have the correct Python version installed.
- If ChromeDriver compatibility issues occur, update it using:
  ```sh
  pip install --upgrade webdriver-manager
  ```
- If login fails, check if the login credentials are correct and update them accordingly.
- If elements are not found, verify the XPaths and update them in the script.

## Disclaimer
This script is intended for educational purposes and should only be used on websites you have permission to scrape.

