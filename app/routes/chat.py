from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from app.schemas.request_model import ChatRequest, ChatResponse
from app.chains.qa_chain import qa_chain
from app.chains.agent_chain import agent_chain
from app.memory.session_memory import memory_manager
from app.ingest.vector_store import vector_store

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for asking questions to the AI assistant.
    
    - **use_rag**: Use RAG pipeline for document-based answers
    - **use_agent**: Use LangChain agent with tools for complex reasoning
    """
    try:
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Update session memory with provided history
        session_memory = memory_manager.get_session("default")
        for message in request.history:
            session_memory.add_message(message.role, message.content)
        
        # Choose chain based on request
        if request.use_agent:
            # Use agent with tools
            result = agent_chain.get_answer(question)
            return ChatResponse(
                answer=result["answer"],
                reasoning=result.get("reasoning"),
                metadata=result.get("metadata", {})
            )
        elif request.use_rag:
            # Use RAG pipeline
            result = qa_chain.get_answer(question)
            return ChatResponse(
                answer=result["answer"],
                sources=result.get("sources", []),
                metadata=result.get("metadata", {})
            )
        else:
            # Simple LLM response without RAG
            result = qa_chain.get_simple_answer(question)
            return ChatResponse(
                answer=result,
                metadata={"model": "simple_llm"}
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.get("/memory/{session_id}")
async def get_memory(session_id: str = "default"):
    """Get conversation memory for a session."""
    try:
        session_memory = memory_manager.get_session(session_id)
        messages = session_memory.get_messages_as_dict()
        return {
            "session_id": session_id,
            "messages": messages,
            "message_count": len(messages)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving memory: {str(e)}")

@router.delete("/memory/{session_id}")
async def clear_memory(session_id: str = "default"):
    """Clear conversation memory for a session."""
    try:
        memory_manager.clear_session(session_id)
        return {"message": f"Memory cleared for session: {session_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing memory: {str(e)}")

@router.get("/tools")
async def get_available_tools():
    """Get information about available tools."""
    try:
        tools_info = agent_chain.get_tools_info()
        return {
            "tools": tools_info,
            "total_tools": len(tools_info)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving tools: {str(e)}")

@router.get("/stats")
async def get_chat_stats():
    """Get statistics about the chat system."""
    try:
        vector_stats = vector_store.get_collection_stats()
        return {
            "vector_store": vector_stats,
            "memory_sessions": len(memory_manager.sessions),
            "available_tools": len(agent_chain.tools)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}") 