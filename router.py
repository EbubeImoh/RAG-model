import re

def route_query(query: str) -> str:
    query_lower = query.lower()

    if re.search(r"\b(company|profile|core values|vision|mission|about)\b", query_lower):
        return "vectorstore"
    
    elif re.search(r"\b(show|list|get|count|how many|employees|orders|transactions|sales)\b", query_lower):
        return "database"

    else:
        return "web"
