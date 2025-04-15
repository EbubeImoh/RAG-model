from query_router.router import route_query

if __name__ == "__main__":
    while True:
        query = input("Ask a question: ")
        if query.lower() in ["exit", "quit"]:
            break
        response = route_query(query)
        print(f"Response: {response}")
