"""
Vector Database Handler using Pinecone
Manages document storage and retrieval for RAG-based responses
"""

from pinecone import Pinecone, ServerlessSpec, PineconeException
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import time
import logging
from backend.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class VectorDatabase:
    """Handles all vector database operations with Pinecone"""

    def __init__(self):
        """Initialize Pinecone connection and embedding model"""
        self.pc: Optional[Pinecone] = None
        self.index = None
        self.embedding_model = None
        self.is_connected = False
        
        self._initialize_service()

    def _initialize_service(self):
        """Initialize connection to Pinecone and load model"""
        try:
            if not settings.PINECONE_API_KEY:
                logger.warning("Pinecone API Key not found. Vector DB features will be disabled.")
                return

            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Load embedding model (lazy load could be better but eager is fine here)
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}...")
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
            
            self._ensure_index_exists()
            self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
            self.is_connected = True
            logger.info("Vector Database initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Vector DB: {e}")
            self.is_connected = False

    def _ensure_index_exists(self):
        """Create Pinecone index if it doesn't exist"""
        try:
            existing_indexes = [i.name for i in self.pc.list_indexes()]
            
            if settings.PINECONE_INDEX_NAME not in existing_indexes:
                logger.info(f"Creating new Pinecone index: {settings.PINECONE_INDEX_NAME}")
                self.pc.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=settings.EMBEDDING_DIMENSION,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud=settings.PINECONE_CLOUD,
                        region=settings.PINECONE_REGION
                    )
                )
                # Wait for index to be ready
                time.sleep(10)
        except PineconeException as e:
            logger.error(f"Pinecone error: {e}")
            raise

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for given text"""
        if not self.embedding_model:
            raise RuntimeError("Embedding model not initialized")
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()

    def store_knowledge(self, text: str, metadata: Dict = None) -> str:
        """Store text and its embedding in Pinecone"""
        if not self.is_connected:
            raise RuntimeError("Vector DB not connected")

        try:
            embedding = self.generate_embedding(text)
            vector_id = f"doc_{{int(time.time() * 1000)}}"
            
            if metadata is None:
                metadata = {}
            metadata['text'] = text
            metadata['timestamp'] = time.time()

            self.index.upsert(
                vectors=[{
                    'id': vector_id,
                    'values': embedding,
                    'metadata': metadata
                }]
            )
            return vector_id

        except Exception as e:
            logger.error(f"Error storing knowledge: {e}")
            raise

    def search_similar(self, query: str, top_k: int = None) -> List[Dict]:
        """Search for similar documents"""
        if not self.is_connected:
            logger.warning("Search attempted but Vector DB not connected")
            return []

        try:
            embedding = self.generate_embedding(query)
            
            results = self.index.query(
                vector=embedding,
                top_k=top_k or settings.TOP_K_RESULTS,
                include_metadata=True
            )

            similar_docs = []
            for match in results.matches:
                similar_docs.append({
                    'id': match.id,
                    'score': match.score,
                    'text': match.metadata.get('text', ''),
                    'metadata': match.metadata
                })

            return similar_docs

        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []

    def get_context_for_query(self, query: str) -> str:
        """Retrieve relevant context formatted for LLM"""
        docs = self.search_similar(query)
        if not docs:
            return ""

        context_parts = []
        for doc in docs:
            # Only include if relevance is high enough
            if doc['score'] > 0.3:
                context_parts.append(f"- {doc['text']}")
        
        return "\n".join(context_parts)

# Singleton instance
vector_db_instance = VectorDatabase()

def get_vector_db() -> VectorDatabase:
    return vector_db_instance