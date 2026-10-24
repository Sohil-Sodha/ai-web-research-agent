# AI Web Research Agent

A Python command-line application that will research a question using
web search, collect information from several sources, and use Google's
Gemini AI to write a useful answer with links to the sources.

> **Status: Stage 2 – web search.**
> The app asks for a research question, searches the web with Tavily,
> and shows the top results (title, URL, snippet). Reading full web
> pages and Gemini-written answers will be added in later stages.

## Requirements

- Python 3.9 or newer
- A Tavily API key (needed now, for web search): https://app.tavily.com
- A Gemini API key (needed in a later stage): https://aistudio.google.com/apikey

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

### 4. Get a Tavily API key

1. Create a free account at https://app.tavily.com
2. Copy your API key from the dashboard (it usually starts with `tvly-`).

### 5. Configure environment variables

Open the `.env` file and replace the placeholders with your own keys:

```
TAVILY_API_KEY=your_tavily_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

Only `TAVILY_API_KEY` is needed at this stage. Write the key without
quotes or spaces around the `=`.

The `.env` file is listed in `.gitignore`, so it will not be committed
to Git. Never share your key or paste it into code.

## Run the app

```bash
python app.py
```

(On some systems the command is `python3 app.py`.)

Type a research question when asked. The app prints up to 5 results,
each with a title, URL, and a short snippet.

If something goes wrong (missing key, no internet, empty question), the
app prints a short explanation instead of crashing.

## Project structure

| File               | Purpose                                         |
|--------------------|-------------------------------------------------|
| `app.py`           | Asks for a question and displays the results    |
| `search_service.py`| Runs the Tavily web search and cleans results   |
| `config.py`        | Reads and validates environment variables       |
| `.env`             | Your local secrets (not committed to Git)       |
| `.gitignore`       | Tells Git which files to ignore                 |
| `requirements.txt` | Python packages the project needs               |
| `README.md`        | This documentation                              |
