# AI Web Research Agent

A Python command-line application that will research a question using
web search, collect information from several sources, and use Google's
Gemini AI to write a useful answer with links to the sources.

> **Status: Stage 3 – webpage content extraction.**
> The app asks for a research question, searches the web with Tavily,
> shows the top results (title, URL, snippet), and can extract the
> readable text of the pages you choose. Gemini-written answers will be
> added in a later stage.

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

1. Type a research question when asked. The app prints up to 5 results,
   each with a title, URL, and a short snippet.
2. The app then asks which results to read in full. Type result numbers
   separated by commas (for example `1,3`), type `all`, or press Enter to
   skip.
3. For each chosen page, the app prints the source title, its URL, and
   the page's main text (shortened to about 3,000 characters).

If a page cannot be read (blocked, not found, timeout, mostly images),
the app explains why and continues with the next page. Other problems
(missing key, no internet, empty question) also print a short
explanation instead of crashing.

Note: some pages cannot be extracted, such as PDFs, pages that need
JavaScript to show their text, and sites that block automated access.
Downloads are limited to 2 MB per page and wait at most about 10 seconds
for a response.

## Project structure

| File               | Purpose                                         |
|--------------------|-------------------------------------------------|
| `app.py`           | Asks for a question and displays the results    |
| `search_service.py`| Runs the Tavily web search and cleans results   |
| `content_extractor.py` | Downloads a page and extracts its readable text |
| `config.py`        | Reads and validates environment variables       |
| `.env`             | Your local secrets (not committed to Git)       |
| `.gitignore`       | Tells Git which files to ignore                 |
| `requirements.txt` | Python packages the project needs               |
| `README.md`        | This documentation                              |
