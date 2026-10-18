from pinecone import Pinecone

from src.config import PINECONE_API_KEY, PINECONE_INDEX_NAME


class VectorStore:

    def __init__(self):
        self.client = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self.client.Index(PINECONE_INDEX_NAME)

    def upsert_chunks(self, chunks, embeddings):
        vectors = []

        for chunk, embedding in zip(chunks, embeddings):
            vectors.append({
                "id": chunk["chunk_id"],
                "values": embedding,
                "metadata": {
                    "source": chunk["source"],
                    "content": chunk["content"]
                }
            })

        if vectors:
            self.index.upsert(vectors=vectors)

        print(f"Vectors submitted to Pinecone: {len(vectors)}")

    def search(self, query_embedding, top_k=3):
        response = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        return response.matches