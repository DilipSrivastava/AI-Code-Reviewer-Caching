from src.document_loader import DocumentLoader
from src.document_chunker import DocumentChunker
from src.embedding_generator import EmbeddingGenerator
from src.vector_store import VectorStore


def main():
    print("Starting knowledge-base load...")

    # Step 1: Load documents
    loader = DocumentLoader()
    documents = loader.load_documents()
    print(f"Documents loaded: {len(documents)}")

    # Step 2: Split documents into chunks
    chunker = DocumentChunker()
    chunks = chunker.chunk_documents(documents)
    print(f"Chunks created: {len(chunks)}")

    if not chunks:
        print("No chunks found. knowledge-base load stopped.")
        return

    # Step 3: Generate embeddings
    embedding_generator = EmbeddingGenerator()
    embeddings = []

    for chunk in chunks:
        embedding = embedding_generator.generate_embedding(
            chunk["content"]
        )
        embeddings.append(embedding)

    print(f"Embeddings generated: {len(embeddings)}")

    # Step 4: Store chunks and embeddings in Pinecone
    vector_store = VectorStore()
    vector_store.upsert_chunks(chunks, embeddings)

    print("Knowledge-base load completed successfully.")


if __name__ == "__main__":
    main()