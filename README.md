# AI Web Research Agent

A Python command-line application that will research a question using
web search, collect information from several sources, and use Google's
Gemini AI to write a useful answer with links to the sources.

> **Status: Stage 1 – project foundation.**
> Right now the app only shows a welcome message. Web search, source
> collection, and Gemini integration will be added in later stages.

## Requirements

- Python 3.9 or newer
- A Gemini API key (needed in later stages): https://aistudio.google.com/apikey

## Setup

### 1. Create a virtual environment

A virtual environment keeps this project's packages separate from the
rest of your computer.

```bash
python -m venv venv
```

### 2. Activate it

- macOS / Linux:
  ```bash
  source venv/bin/activate
  ```
- Windows (Command Prompt):
  ```bat
  venv\Scripts\activate.bat
  ```
- Windows (PowerShell):
  ```powershell
  venv\Scripts\Activate.ps1
  ```

You should see `(venv)` at the start of your terminal prompt.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Open the `.env` file and replace the placeholder with your own key:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

The `.env` file is listed in `.gitignore`, so it will not be committed
to Git. Never share your key or paste it into code.

## Run the app

```bash
python app.py
```

(On some systems the command is `python3 app.py`.)

## Project structure

| File               | Purpose                                         |
|--------------------|-------------------------------------------------|
| `app.py`           | Application entry point                         |
| `config.py`        | Reads settings from environment variables       |
| `.env`             | Your local secrets (not committed to Git)       |
| `.gitignore`       | Tells Git which files to ignore                 |
| `requirements.txt` | Python packages the project needs               |
| `README.md`        | This documentation                              |
