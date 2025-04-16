import logging

logging.basicConfig(filename='logs/queries.log', level=logging.INFO)

def log_query(query: str, user: str, route: str, feedback: str = ""):
    logging.info(f"User: {user} | Route: {route} | Query: {query} | Feedback: {feedback}")
