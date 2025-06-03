from googlesearch import search


def search_google(query: str, num_results: int = 10):
    """
    Search Google for a query.

    Args:
        query: The query to search for.
        num_results: The number of results to return.

    Returns:
        A list of search results.
    """
    results = list(search(query, advanced=True, num_results=num_results))
    return results
