"""Semantic Search Service — FAISS + sentence-transformers (lazy imports)."""

import os
import pickle
import logging
from typing import Optional, List, Any

from app.core.config import get_settings
from app.schemas.recommendation import SemanticSearchResult

settings = get_settings()
logger = logging.getLogger(__name__)


class SemanticSearchService:
    """Vector-based semantic search using FAISS and sentence-transformers."""

    _instance: Optional["SemanticSearchService"] = None

    def __init__(self) -> None:
        self._model: Any = None
        self._index: Any = None
        self._movie_ids: List[int] = []
        self._movie_titles: List[str] = []
        self._movie_overviews: List[str] = []
        self._movie_posters: List[str] = []
        self._initialized = False

    @classmethod
    async def get_instance(cls) -> "SemanticSearchService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def initialize(self) -> None:
        """Load the sentence-transformer model and FAISS index."""
        if self._initialized:
            return

        try:
            # Lazy imports — these are optional heavy dependencies
            import faiss
            from sentence_transformers import SentenceTransformer

            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self._model = SentenceTransformer(settings.EMBEDDING_MODEL)

            # Load FAISS index if it exists
            index_path = settings.FAISS_INDEX_PATH
            if os.path.exists(index_path):
                logger.info(f"Loading FAISS index from {index_path}")
                self._index = faiss.read_index(index_path)

                # Load movie metadata (stored alongside index)
                meta_path = index_path.replace(".bin", "_meta.pkl")
                if os.path.exists(meta_path):
                    with open(meta_path, "rb") as f:
                        meta = pickle.load(f)
                    self._movie_ids = meta.get("ids", [])
                    self._movie_titles = meta.get("titles", [])
                    self._movie_overviews = meta.get("overviews", [])
                    self._movie_posters = meta.get("posters", [])
            else:
                logger.warning(
                    f"FAISS index not found at {index_path}. "
                    "Semantic search will return empty results until index is built."
                )

            self._initialized = True
            logger.info("SemanticSearchService initialized successfully")

        except ImportError as e:
            logger.warning(
                f"⚠️ ML dependencies not installed ({e}). "
                "Semantic search disabled. Install sentence-transformers and faiss-cpu to enable."
            )
            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize SemanticSearchService: {e}")
            self._initialized = True  # Mark as initialized to avoid retry loops

    async def search(self, query: str, limit: int = 10) -> List[SemanticSearchResult]:
        """
        Encode a natural language query and find nearest neighbors in FAISS.

        Returns:
            List of SemanticSearchResult with similarity scores
        """
        if self._model is None or self._index is None:
            logger.warning("Semantic search not available — model or index not loaded")
            return []

        try:
            import numpy as np

            # Encode query
            query_vector = self._model.encode([query], normalize_embeddings=True)
            query_vector = np.array(query_vector, dtype=np.float32)

            # Search FAISS
            distances, indices = self._index.search(query_vector, min(limit, self._index.ntotal))

            results: List[SemanticSearchResult] = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < 0 or idx >= len(self._movie_ids):
                    continue

                results.append(
                    SemanticSearchResult(
                        movie_id=self._movie_ids[idx],
                        title=self._movie_titles[idx] if idx < len(self._movie_titles) else "Unknown",
                        overview=self._movie_overviews[idx] if idx < len(self._movie_overviews) else None,
                        similarity_score=round(float(1 - dist), 4),
                        poster_path=self._movie_posters[idx] if idx < len(self._movie_posters) else None,
                    )
                )

            return results

        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []

    async def build_index(
        self,
        movie_ids: List[int],
        texts: List[str],
        titles: List[str],
        overviews: List[str],
        posters: List[str],
    ) -> None:
        """Build and save a new FAISS index from movie texts."""
        import faiss
        import numpy as np

        if self._model is None:
            raise RuntimeError("Model not loaded. Call initialize() first.")

        logger.info(f"Building FAISS index for {len(texts)} movies...")

        # Encode all texts
        embeddings = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
        embeddings = np.array(embeddings, dtype=np.float32)

        # Build FAISS index (Inner Product for cosine similarity on normalized vectors)
        dimension = embeddings.shape[1]
        self._index = faiss.IndexFlatIP(dimension)
        self._index.add(embeddings)

        # Store metadata
        self._movie_ids = movie_ids
        self._movie_titles = titles
        self._movie_overviews = overviews
        self._movie_posters = posters

        # Save to disk
        index_path = settings.FAISS_INDEX_PATH
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(self._index, index_path)

        meta_path = index_path.replace(".bin", "_meta.pkl")
        with open(meta_path, "wb") as f:
            pickle.dump(
                {
                    "ids": movie_ids,
                    "titles": titles,
                    "overviews": overviews,
                    "posters": posters,
                },
                f,
            )

        logger.info(f"FAISS index saved with {self._index.ntotal} vectors")
