"""
app.py - Entry point of the AI Web Research Agent.
 
Stage 3: asks for a question, searches the web, shows the results, and
lets the user pick results whose page text should be extracted.
Search logic lives in search_service.py; extraction in content_extractor.py.
"""

import content_extractor
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


def parse_selection(answer, count):
    """Turn input like "1,3" or "all" into a list of 0-based positions.
 
    Returns an empty list if the input is blank. Returns None if it is
    invalid (not numbers, or numbers outside 1..count).
    """
    answer = answer.strip().lower()

    if not answer:
        return []
    
    if answer == "all":
        return list(range(count))
    
    positions = []

    for part in answer.replace(" ", "").split(","):

        if not part.isdigit() or not 1 <= int(part) <= count:
            return None
        
        if int(part) - 1 not in positions:
            positions.append(int(part) - 1)

    return positions


def ask_which_results(results):
    """Ask the user which results to extract; return the chosen results."""
    while True:
        try:
            answer = input(
                "Extract page text from which results? "
                "(e.g. 1,3 or all; press Enter to skip) "
            )

        except [EOFError, KeyboardInterrupt]:
            print()
            return []
        
        positions = parse_selection(answer, len(results))

        if positions is not None:
            return [results[i] for i in positions]
        
        print(f"Please enter numbers between 1 and {len(results)}, separated by commas.")


def show_extracted_text(results):
    """Extract and print the text of each chosen result.
 
    A failure on one page is reported and the next page is still processed.
    """
    for result in results:
        print("\n" + "=" * 50)
        print(f"Source: {result['title']}")
        print(f"URL: {result['url']}")
        print("-" * 50)

        try:
            print(content_extractor.extract_content(result["url"]))

        except content_extractor.ExtractionError as error:
            print(f"Could not extract this page: {error}")

    print("=" * 50)


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
        return
    
    show_results(results)
    
    if not results:
        return
    
    chosen = ask_which_results(results)

    if chosen:
        print(f"\nExtracting text from {len(chosen)} page(s)...")
        show_extracted_text(chosen)

# This block runs main() only when you start this file directly
# (python app.py), not when it is imported by another file.
if __name__ == "__main__":
    main()