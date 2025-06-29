# Playwright Error Reporter with Gemini Integration

This project is a test automation framework using [Playwright](https://playwright.dev/) and Python. It automatically captures errors during test execution and sends detailed reports to Google's Gemini model. The Gemini model then attempts to generate a fixed version of the test file based on the error message and page DOM. This has been developed mainly as a POC (proof-of-concept) project, feel free to fork and create full scale projects.

## Features

- 🚀 Automated UI testing with Playwright
- 🧠 Error analysis and fix suggestions using Gemini
- 🧾 Captures:
  - The DOM at the time of error
  - The error message
  - The path of the file where the error occurred
- 🛠️ Automatically generates a fixed test file using AI

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/sandeepjacob-20/PlaywrightSelfHealerAI.git
cd your-repo-name
```
### 2. Install Python Requirements

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

```bash
playwright install
```

### 4. Add Your Gemini API Key

Set your Gemini API key as an environment variable before running the tests:

#### Linux/macOS

```bash
export API_KEY="your_api_key_here"
```

#### Windows (Command Prompt)

```cmd
set API_KEY=your_api_key_here
```

#### Windows (PowerShell)

```powershell
$env:API_KEY="your_api_key_here"
```

Alternatively for linux, You can add the API key by running the set_api_key.bash script:

```bash
bash set_api_key.bash
```

You can get a free API key from https://aistudio.google.com/apikey 

## Usage

Run your tests as you normally would. On encountering an error:

- The script will capture the **error message**, **DOM**, and **file path**.
- This information is sent to **Gemini**.
- Gemini returns a suggested fix, which is saved as a **new file**.

### Example

```bash
python automation.py
```

Fixed files are saved in the ./fixed_files/ directory.
