
import hashlib
import json
import sqlite3
import time
from pathlib import Path

from openai import OpenAI
from src.config import OPENAI_API_KEY


class EmbeddingGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "text-embedding-3-small"

        self.cache_path = Path(__file__).resolve().parent.parent / "embedding_cache.db"
        self._initialize_cache()

        self.cache_hits = 0
        self.cache_misses = 0
        self.api_calls = 0

    def _initialize_cache(self):
        with sqlite3.connect(self.cache_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS embeddings (
                    cache_key TEXT PRIMARY KEY,
                    embedding TEXT NOT NULL
                )
            """)

    def _get_cache_key(self, text):
        content = f"{self.model}:{text}"
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def generate_embedding(self, text):
        cache_key = self._get_cache_key(text)

        # Check SQLite cache
        with sqlite3.connect(self.cache_path) as conn:
            row = conn.execute(
                "SELECT embedding FROM embeddings WHERE cache_key = ?",
                (cache_key,)
            ).fetchone()

        if row:
            self.cache_hits += 1
            print(f"Embedding cache HIT | Hits: {self.cache_hits}")
            return json.loads(row[0])

        # IF No Data in Cache Then call OpenAI to create embedding
        self.cache_misses += 1
        self.api_calls += 1
        print(f"Embedding cache MISS | API calls: {self.api_calls}")

        start_time = time.perf_counter()

        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )

        embedding = response.data[0].embedding

        elapsed = time.perf_counter() - start_time
        print(f"Embedding API time: {elapsed:.4f} seconds")

        # Save embedding to SQLite
        with sqlite3.connect(self.cache_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO embeddings (cache_key, embedding)
                VALUES (?, ?)
                """,
                (cache_key, json.dumps(embedding))
            )

        return embedding
