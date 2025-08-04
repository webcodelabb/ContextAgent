from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Message(BaseModel):
    """Individual message in conversation history."""
    role: str = Field(..., description="Role of the message sender (user/agent)")
    content: str = Field(..., description="Content of the message")

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str = Field(..., description="User's question or query")
    history: Optional[List[Message]] = Field(default=[], description="Conversation history")
    use_rag: bool = Field(default=True, description="Whether to use RAG pipeline")
    use_agent: bool = Field(default=False, description="Whether to use LangChain agent")

class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str = Field(..., description="AI assistant's response")
    sources: Optional[List[str]] = Field(default=[], description="Source documents used")
    reasoning: Optional[str] = Field(default=None, description="Agent's reasoning process")
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional metadata")

class DocumentUploadResponse(BaseModel):
    """Response model for document upload."""
    filename: str = Field(..., description="Name of uploaded file")
    status: str = Field(..., description="Upload status")
    message: str = Field(..., description="Status message")
    document_count: Optional[int] = Field(default=None, description="Number of documents processed")

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    components: Dict[str, str] = Field(..., description="Component status") 