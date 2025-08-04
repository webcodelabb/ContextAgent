import os
from typing import List, Dict, Any, Optional
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from app.ingest.embedder import embedder
from app.utils.config import settings

class VectorStore:
    """Manages document storage and retrieval using ChromaDB."""
    
    def __init__(self):
        self.persist_directory = settings.CHROMA_PERSIST_DIRECTORY
        self.embedding_function = embedder.embeddings
        self.vector_store = None
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize or load the vector store."""
        if os.path.exists(self.persist_directory):
            # Load existing vector store
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_function
            )
        else:
            # Create new vector store
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_function
            )
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        if not documents:
            return
        
        # Process documents through embedder
        processed_docs = embedder.process_documents(documents)
        
        # Add to vector store
        self.vector_store.add_documents(processed_docs)
        self.vector_store.persist()
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Search for similar documents."""
        if not self.vector_store:
            return []
        
        return self.vector_store.similarity_search(query, k=k)
    
    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        """Search for similar documents with similarity scores."""
        if not self.vector_store:
            return []
        
        return self.vector_store.similarity_search_with_score(query, k=k)
    
    def get_relevant_documents(self, query: str, k: int = 4) -> List[Document]:
        """Get relevant documents for a query (alias for similarity_search)."""
        return self.similarity_search(query, k)
    
    def delete_collection(self) -> None:
        """Delete the entire collection."""
        if self.vector_store:
            self.vector_store.delete_collection()
            self.vector_store = None
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        if not self.vector_store:
            return {"count": 0, "status": "not_initialized"}
        
        try:
            count = self.vector_store._collection.count()
            return {
                "count": count,
                "status": "active",
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            return {"count": 0, "status": f"error: {str(e)}"}

# Global vector store instance
vector_store = VectorStore() 