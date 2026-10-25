"""
search_service.py - Web search using the Tavily API.
 
This file only talks to Tavily and cleans up the results.
It does not print anything; app.py decides how to show results.
"""

import requests
from tavily import TavilyClient

from tavily.errors import (
    BadRequestError,
    ForbiddenError,
    InvalidAPIKeyError,
    TimeoutError as TavilyTimeoutError,
    UsageLimitExceededError,
)

import config

# How many results to request. Kept small so output is easy to read.
MAX_RESULTS = 5


class SearchError(Exception):
    """A search problem, with a message that is safe to show the user."""
    pass

def search(question):
    """Search the web for `question` and return a list of result dicts.
 
    Each result has the keys: title, url, snippet.
    Raises SearchError with a friendly message if something goes wrong.
    """
    question = (question or "").strip()

    if not question:
        raise SearchError("Please enter a question to research.")
    
    # Validate the key first so we never call the API without one.
    try:
        api_key = config.get_tavily_api_key()

    except ValueError as error:
        raise SearchError(str(error))
    

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(question, max_result=MAX_RESULTS)

    except InvalidAPIKeyError:
        raise SearchError("Tavily rejected your API key. Check TAVILY_API_KEY in .env.")
    
    except ForbiddenError:
        raise SearchError("Tavily refused this request. Check your account and key permissions.")
    
    except UsageLimitExceededError:
        raise SearchError("Your Tavily usage limit was reached. Check your plan or try later.")
    
    except BadRequestError:
        raise SearchError("Tavily could not understand this search. Try rewording your question.")
    
    except (TavilyTimeoutError, requests.exceptions.Timeout):
        raise SearchError("Network problem. Check your internet connection and try again.")
    
    except Exception as error:
        # Only the error's type name is shown, in case the message has sensitive details.
        raise SearchError(f"Unexpected search error ({type(error).__name__}).")
    
    return _clean_results(response)


def _clean_results(response):
    """Turn Tavily's raw response into simple dicts, filling in missing fields."""
    results = []

    for item in (response or {}).get("results") or []:
        results.append(
            {
                "title": item.get("title") or "(no title)",
                "url": item.get("url") or "(no URL)",
                "snippet": (
                    item.get("content")
                    or item.get("snippet")
                    or "(no snippet available)"
                ),
            }
        )

    return results