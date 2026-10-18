from src.embedding_generator import EmbeddingGenerator
from src.vector_store import VectorStore


class Retriever:

    def __init__(self, top_k=3):
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore()
        self.top_k = top_k

    def retrieve(self, query):
        # Step 1: Generate embedding for the query
        query_embedding = self.embedding_generator.generate_embedding(query)

        # Step 2: Search Pinecone for relevant guidelines
        matches = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=self.top_k
        )

        # Step 3: Extract the retrieved content
        results = []

        for match in matches:
            results.append({
                "score": match.score,
                "source": match.metadata.get("source", "Unknown"),
                "content": match.metadata.get("content", "")
            })

        return results