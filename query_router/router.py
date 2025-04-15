from vectorstore.vector_search import search_vectorstore
from database.schema_loader import load_schema
from query_constructor.text_to_sql import generate_sql_query
from fallback.not_found import fallback_response

def route_query(user_query):
    schema = load_schema()
    
    # Check for answer in vectorstore
    vector_result = search_vectorstore(user_query)
    if vector_result:
        return vector_result
    
    # Attempt SQL translation
    sql_query = generate_sql_query(user_query, schema)
    if sql_query:
        return sql_query
    
    return fallback_response()
