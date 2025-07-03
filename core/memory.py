"""
Memory module for vector DB operations using Chroma.
"""
from typing import List, Optional
import chromadb
from core.utils import logger, load_config

class Memory:
    """
    Wraps Chroma vector DB for ingesting and querying embeddings.
    """
    def __init__(self) -> None:
        self.config = load_config()
        try:
            persistent_path = self.config.get('memory', {}).get('persistent_client_path', './data/chroma_db')
            self.client = chromadb.PersistentClient(path=persistent_path)
            self.collection = self.client.create_collection(self.config.get('memory', {}).get('collection', 'default'))
        except Exception as e:
            logger.error(f"Failed to initialize Chroma DB: {e}")
            raise

    def ingest(self, embedding: List[float], metadata: dict) -> bool:
        """
        Ingests an embedding and its metadata into the vector DB.

        Args:
            embedding (List[float]): The embedding vector.
            metadata (dict): Associated metadata.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # TODO : which embedding ? do a benchmarck ?
            self.collection.add(embeddings=[embedding], metadatas=[metadata])
            logger.info("Embedding ingested successfully.")
            return True
        except Exception as e:
            logger.error(f"Ingest failed: {e}")
            return False

    def query(self, embedding: List[float], n_results: int = 1) -> Optional[List[dict]]:
        """
        Queries the vector DB for similar embeddings.

        Args:
            embedding (List[float]): The query embedding.
            n_results (int): Number of results to return.

        Returns:
            Optional[List[dict]]: List of matching metadata dicts, or None if failed.
        """
        try:
            # TODO : which method for queries ?
            results = self.collection.query(query_embeddings=[embedding], n_results=n_results)
            return results.get('metadatas')
        except Exception as e:
            logger.error(f"Query failed: {e}")
            return None 