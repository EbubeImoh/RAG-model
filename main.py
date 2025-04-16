from query_engine import load_vectorstore, get_qa_chain
from logs.logger import log_query
from router import route_query
from db.database import execute_sql_query
from web.web_search import search_web
from auth.access import is_authorized
from db.database import generate_sql

vectorstore = load_vectorstore()
qa_chain = get_qa_chain(vectorstore)

def handle_query(query: str, user: str = "anonymous", role: str = "guest", feedback: str = ""):
    route = route_query(query)

    if not is_authorized(role, route):
        return {
            "source": "Access Denied",
            "response": f"User with role '{role}' is not allowed to access '{route}' resources."
        }

    if route == "vectorstore":
        response = qa_chain.run(query)

    elif route == "database":
        try:
            sql_query = generate_sql(query)
            result = execute_sql_query(sql_query)
            response = f"SQL: {sql_query}\n\nResult: {result}"
        except Exception as e:
            response = f"SQL error: {str(e)}"

    elif route == "web":
        response = search_web(query)

    else:
        response = "Unknown route."

    log_query(query, user, route, feedback)

    return {
        "source": route,
        "response": response
    }
