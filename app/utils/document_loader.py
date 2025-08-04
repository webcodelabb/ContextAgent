import os
from typing import List, Optional
from langchain.schema import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    Docx2txtLoader
)
from app.utils.config import settings

class DocumentLoader:
    """Handles loading documents from various file formats."""
    
    @staticmethod
    def load_document(file_path: str) -> List[Document]:
        """Load a single document based on its file extension."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension not in settings.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        try:
            if file_extension == ".pdf":
                loader = PyPDFLoader(file_path)
            elif file_extension == ".txt":
                loader = TextLoader(file_path, encoding="utf-8")
            elif file_extension == ".md":
                loader = UnstructuredMarkdownLoader(file_path)
            elif file_extension == ".docx":
                loader = Docx2txtLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
            
            documents = loader.load()
            
            # Add metadata
            for doc in documents:
                doc.metadata["source"] = os.path.basename(file_path)
                doc.metadata["file_path"] = file_path
                doc.metadata["file_type"] = file_extension
            
            return documents
            
        except Exception as e:
            raise Exception(f"Error loading document {file_path}: {str(e)}")
    
    @staticmethod
    def load_documents_from_directory(directory_path: str) -> List[Document]:
        """Load all supported documents from a directory."""
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        documents = []
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            if os.path.isfile(file_path):
                file_extension = os.path.splitext(filename)[1].lower()
                
                if file_extension in settings.SUPPORTED_EXTENSIONS:
                    try:
                        docs = DocumentLoader.load_document(file_path)
                        documents.extend(docs)
                    except Exception as e:
                        print(f"Warning: Could not load {filename}: {e}")
        
        return documents
    
    @staticmethod
    def validate_file(file_path: str) -> bool:
        """Validate if a file can be processed."""
        if not os.path.exists(file_path):
            return False
        
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in settings.SUPPORTED_EXTENSIONS:
            return False
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > settings.MAX_FILE_SIZE:
            return False
        
        return True

# Global document loader instance
document_loader = DocumentLoader() 