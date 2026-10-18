from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:

    def __init__(self, chunk_size=500, chunk_overlap=100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def chunk_documents(self, documents):
        chunks = []

        for document in documents:
            text_chunks = self.splitter.split_text(document["content"])

            for index, text in enumerate(text_chunks):
                chunks.append({
                    "chunk_id": f"{document['source']}_{index}",
                    "source": document["source"],
                    "content": text
                })
        print(f"Total chunks created: {len(chunks)}")
        print(f"chunks Are: {chunks}")
        return chunks
