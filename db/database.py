from langchain.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from db.schema import fetch_db_schema  # this is the function you provided

llm = Ollama(model="tinyllama")

template = """
You are a PostgreSQL expert. Use the schema below to write an accurate SQL query from the question.

Schema:
{schema}

Question:
{question}

Only use the tables and columns listed above. Output only the SQL query, nothing else.
"""

prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template=template
)
sql_chain = LLMChain(llm=llm, prompt=prompt)

from db.schema import fetch_db_schema  # Import the function from schema.py

def generate_sql(nl_query: str) -> str:
    schema = fetch_db_schema()  # Fetch the schema dynamically
    return sql_chain.run({"schema": schema, "question": nl_query})
