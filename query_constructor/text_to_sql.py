from utils.llm import call_llm

def generate_sql_query(user_query, schema):
    prompt = f"Using the schema: {schema}, convert the following question to SQL: {user_query}"
    response = call_llm(prompt)
    return response
