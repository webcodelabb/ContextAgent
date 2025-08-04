import os
import tempfile
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
from app.schemas.request_model import DocumentUploadResponse
from app.utils.document_loader import document_loader
from app.ingest.vector_store import vector_store
from app.utils.config import settings

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document for the RAG system.
    
    Supported formats: PDF, TXT, MD, DOCX
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in {".pdf", ".txt", ".md", ".docx"}:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file_extension}. Supported: PDF, TXT, MD, DOCX"
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Load document
            documents = document_loader.load_document(temp_file_path)
            
            # Add to vector store
            vector_store.add_documents(documents)
            
            return DocumentUploadResponse(
                filename=file.filename,
                status="success",
                message=f"Successfully processed {len(documents)} document chunks",
                document_count=len(documents)
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        return DocumentUploadResponse(
            filename=file.filename if file.filename else "unknown",
            status="error",
            message=f"Error processing document: {str(e)}",
            document_count=0
        )

@router.post("/directory")
async def ingest_directory(directory_path: str):
    """
    Ingest all supported documents from a directory.
    """
    try:
        if not os.path.exists(directory_path):
            raise HTTPException(status_code=404, detail=f"Directory not found: {directory_path}")
        
        # Load documents from directory
        documents = document_loader.load_documents_from_directory(directory_path)
        
        if not documents:
            return JSONResponse(
                status_code=200,
                content={
                    "message": "No supported documents found in directory",
                    "directory": directory_path,
                    "document_count": 0
                }
            )
        
        # Add to vector store
        vector_store.add_documents(documents)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": f"Successfully processed {len(documents)} documents",
                "directory": directory_path,
                "document_count": len(documents)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting directory: {str(e)}")

@router.get("/stats")
async def get_ingestion_stats():
    """Get statistics about ingested documents."""
    try:
        vector_stats = vector_store.get_collection_stats()
        return {
            "vector_store": vector_stats,
            "supported_formats": list({".pdf", ".txt", ".md", ".docx"}),
            "max_file_size_mb": settings.MAX_FILE_SIZE // (1024 * 1024)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")

@router.delete("/clear")
async def clear_documents():
    """Clear all ingested documents from the vector store."""
    try:
        vector_store.delete_collection()
        return {"message": "All documents cleared from vector store"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing documents: {str(e)}") 