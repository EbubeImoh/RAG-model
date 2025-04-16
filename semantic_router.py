from sentence_transformers import SentenceTransformer, util
from routing_labels import routing_labels

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def route_question(question: str, threshold: float = 0.4):
    question_embedding = model.encode(question, convert_to_tensor=True)
    
    similarities = {}
    for label, description in routing_labels.items():
        desc_embedding = model.encode(description, convert_to_tensor=True)
        sim_score = float(util.pytorch_cos_sim(question_embedding, desc_embedding))
        similarities[label] = sim_score

    # Choose the highest similarity route
    best_route = max(similarities, key=similarities.get)

    # Optional: enforce threshold to fall back to web if uncertain
    if similarities[best_route] < threshold:
        return "web"
    
    return best_route, similarities