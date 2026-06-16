# 🎓 NUST LMS Archiver (Moodle Automation Bot)

![Python](https://img.shields.io/badge/python-3.14-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=Playwright&logoColor=white)
![Asyncio](https://img.shields.io/badge/Asyncio-000000?style=for-the-badge&logo=Python&logoColor=white)

A fully asynchronous web automation tool built with Python and Playwright. This bot securely logs into Moodle-based university portals (specifically configured for NUST LMS), navigates complex DOM structures, handles lazy-loading, and mass-downloads your entire academic history into neatly organized, course-specific local folders. 

Turn a 10-hour manual chore into a 2-minute automated script. 🤖

---

## ✨ Features

* **🏃‍♂️ Fully Asynchronous:** Built with `asyncio` and `playwright.async_api` for rapid, non-blocking page navigation and downloads.
* **📜 Smart Lazy-Load Handling:** Automatically simulates user scrolling to trigger background AJAX requests, ensuring *all* past courses are loaded before scanning begins.
* **🗂️ Dynamic Archiving:** Automatically parses course titles, sanitizes them for OS compatibility, and generates a clean subfolder directory structure for your files.
* **🔐 Secure Auth:** Uses local `.env` variables to completely isolate your university credentials from the source code.
* **🛑 Polite Rate-Limiting:** Incorporates randomized `asyncio.sleep()` delays to mimic human interaction and avoid overwhelming university servers.

---

## 🎥 See it in Action

<img width="1280" height="720" alt="NUST-LMS-Archiver-2" src="https://github.com/user-attachments/assets/bc9b342d-f20c-4dbf-9570-5e01b6e31ce2" />



---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have **Python 3.14** installed. 

### 2. Installation
Clone the repository and install the required dependencies using the provided `requirements.txt` file.

```bash
# Clone the repository
git clone https://github.com/FatimaSarwarA/NUST-LMS-Archiver.git
cd NUST-LMS-Archiver

# Install Python dependencies from the requirements file
pip install -r requirements.txt

# Install the Chromium browser for Playwright
playwright install chromium
```
### 3. Configuration
Never hardcode your passwords. Create a hidden `.env` file in the root directory of the project:

```bash
# Windows/VS Code
New-Item .env
# Mac/Linux
touch .env
```
Open the `.env` file and add your credentials:
```plaintext
NUST_USERNAME=your_registration_number
NUST_PASSWORD=your_actual_password
```
### 4. Run the Bot
Make sure you have an active internet connection, plug in your laptop, and let the bot do the heavy lifting.

```bash
python main.py
```
Check your newly created `NUST_Submissions/` folder to see your structured academic archive!

# 🧠 Under the Hood
Moodle portals are notoriously difficult to scrape cleanly due to heavy JavaScript frameworks and nested page structures. This script works by:

Identifying anchor links using CSS selectors (`a.coursename`).

Iterating through the dashboard and utilizing the `expect_download()` event listener to capture Moodle's `forcedownload=1` PHP redirects.

Using string comprehension to sanitize raw DOM text into OS-safe folder paths.

# ⚠️ Disclaimer
This tool is built strictly for educational purposes and personal data archiving. Please use it responsibly. Do not remove the rate-limiting delays, as aggressively spamming your university's LMS server could result in a temporary IP ban from their IT department.
