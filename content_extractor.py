"""
content_extractor.py - Download a webpage and extract its readable text.
 
Two steps:
  1. Download the page with `requests` (so we control timeouts and size).
  2. Extract the main article text with `trafilatura`, which removes
     menus, ads, footers and other clutter.
 
This file does not print anything; app.py decides how to show the text.
"""

from urllib.parse import urlparse

import requests
import trafilatura

# Wait up to 5 seconds to connect and 10 seconds for each chunk of data.
TIMEOUT = (5, 10)

# Stop downloading after 2 MB so a huge page cannot slow us down.
MAX_DOWNLOADE_BYTES = 2 * 1024 * 1024

# Keep only this many characters of text per page (keeps output readable).
MAX_TEXT_CHARS = 3000

# Pages with less text than this are treated as "no readable text".
MIN_TEXT_CHARS = 100

# Some sites block requests that do not look like a browser.
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AIWebResearchAgent/0.3)"}


class ExtractionError(Exception):
    """An extraction problem, with a message that is safe to show the user."""
    pass


def extract_content(url):
    """Return the readable text of the page at `url` (shortened if long).
 
    Raises ExtractionError with a friendly message if anything goes wrong.
    """
    _check_url(url)
    html = _download(url)

    try:
        text = trafilatura.extract(html, include_comments=False, include_tables=False)

    except Exception:
        raise ExtractionError("The page content could not be read.")
    
    text = (text or "").strip()

    if len(text) < MIN_TEXT_CHARS:
        raise ExtractionError(
            "This page has little or no readable text "
            "(it may need JavaScript, a login, or be mostly images)."
        )
    
    return _shorten(text)


def _check_url(url):
    """Make sure the URL looks like a normal web address."""
    parsed = urlparse(url or "")

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ExtractionError("This is not a valid web address (URL).")
    

def _download(url):
    """Download the page and return its raw bytes (at most MAX_DOWNLOAD_BYTES)."""
    try:
        # stream=True lets us read the page in pieces and stop early.
        with requests.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True) as response:
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")

            if content_type and "html" not in content_type and "text" not in content_type:
                raise ExtractionError("This link is not a normal webpage (for example a PDF or image).")
            
            data = b""
            for chunk in response.iter_content(chunk_size=64 * 1024):
                data += chunk
                if len(data) >= MAX_DOWNLOADE_BYTES:
                    data = data[:MAX_DOWNLOADE_BYTES]
                    break

            return data
        
    except requests.exceptions.HTTPError as error:
        status = error.response.status_code if error.response is not None else "unknown"

        if status in (401, 403):
            raise ExtractionError(f"The website blocked access (HTTP {status}).")
        
        if status == 404:
            raise ExtractionError("The page was not found (HTTP 404).")
        
        raise ExtractionError(f"The website returned an error (HTTP {status}).")
    
    except requests.exceptions.Timeout:
        raise ExtractionError("The website took too long to respond (timeout).")
    
    except requests.exceptions.ConnectionError:
        raise ExtractionError("Could not connect to the website. Check your internet connection.")
    
    except requests.exceptions.RequestException:
        raise ExtractionError("The page could not be downloaded.")
    

def _shorten(text):
    """Cut the text to MAX_TEXT_CHARS, ending on a whole word."""
    if len(text) <= MAX_TEXT_CHARS:
        return text
    
    cut = text[:MAX_TEXT_CHARS].rsplit(" ", 1)[0]

    return cut + " ...[text shortened]"
