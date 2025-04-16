from duckduckgo_search import ddg

def search_web(query: str):
    try:
        results = ddg(query, max_results=3)
        if results:
            return "\n\n".join([f"{r['title']}: {r['href']}" for r in results])
        else:
            return "No useful web results found."
    except Exception as e:
        return f"Web search error: {str(e)}"
