from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.utils.config import settings

class DocumentEmbedder:
    """Handles document embedding and text processing."""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model="text-embedding-ada-002"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into smaller chunks for better retrieval."""
        return self.text_splitter.split_documents(documents)
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        return self.embeddings.embed_documents(texts)
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        return self.embeddings.embed_query(text)
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Process documents: split and prepare for vector storage."""
        # Split documents into chunks
        split_docs = self.split_documents(documents)
        
        # Add metadata if not present
        for doc in split_docs:
            if not doc.metadata:
                doc.metadata = {}
            if "source" not in doc.metadata:
                doc.metadata["source"] = "unknown"
        
        return split_docs

# Global embedder instance
embedder = DocumentEmbedder() 