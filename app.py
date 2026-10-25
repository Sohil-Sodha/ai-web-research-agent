"""
app.py - Entry point of the AI Web Research Agent.
 
Stage 2: asks for a question, searches the web, and shows the results.
All search logic lives in search_service.py.
"""

import search_service

# Long snippets are shortened so the terminal output stays readable.
SNIPPET_LIMIT = 300


def show_results(results):
    """Print each search result with its title, URL and snippet."""
    if not results:
        print("No results found. Try rewording your question.")
        return
    
    print(f"\nFound {len(results)} result(s):\n")

    for number, result in enumerate(results, start=1):
        snippet = result["snippet"]

        if len(snippet) > SNIPPET_LIMIT:
            snippet = snippet[:SNIPPET_LIMIT].rstrip() + "..."

        print(f"{number}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   {snippet}\n")


def main():
    """Run the application."""
    print("=" * 50)
    print("  Welcome to the AI Web Research Agent!")
    print("=" * 50)

    try:
        question = input("\nWhat would you like to research?: ")

    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        return
    

    try:
        print("\nSearching the web...")
        results = search_service.search(question)

    except search_service.SearchError as error:
        print(f"\nSorry: {error}")

    
    show_results(results)
    
# This block runs main() only when you start this file directly
# (python app.py), not when it is imported by another file.
if __name__ == "__main__":
    main()