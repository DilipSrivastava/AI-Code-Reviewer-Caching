from pathlib import Path


class DocumentLoader:

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)

    def load_documents(self):
        documents = []

        for file_path in self.data_dir.rglob("*.txt"):
            content = file_path.read_text(encoding="utf-8")

            if content.strip():
                documents.append({
                    "source": str(file_path),
                    "content": content
                })

        return documents