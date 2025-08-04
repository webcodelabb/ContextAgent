from typing import List, Dict, Any
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from app.schemas.request_model import Message

class SessionMemory:
    """Manages conversational memory for chat sessions."""
    
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation memory."""
        if role == "user":
            self.memory.chat_memory.add_user_message(content)
        elif role == "agent":
            self.memory.chat_memory.add_ai_message(content)
    
    def get_messages(self) -> List[BaseMessage]:
        """Get all messages from memory."""
        return self.memory.chat_memory.messages
    
    def get_messages_as_dict(self) -> List[Message]:
        """Get messages in the format expected by the API."""
        messages = []
        for msg in self.memory.chat_memory.messages:
            if isinstance(msg, HumanMessage):
                messages.append(Message(role="user", content=msg.content))
            elif isinstance(msg, AIMessage):
                messages.append(Message(role="agent", content=msg.content))
        return messages
    
    def clear(self) -> None:
        """Clear the conversation memory."""
        self.memory.clear()
    
    def get_memory_variables(self) -> Dict[str, Any]:
        """Get memory variables for LangChain."""
        return self.memory.load_memory_variables({})

class MemoryManager:
    """Manages multiple session memories."""
    
    def __init__(self):
        self.sessions: Dict[str, SessionMemory] = {}
    
    def get_session(self, session_id: str = "default") -> SessionMemory:
        """Get or create a session memory."""
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionMemory(session_id)
        return self.sessions[session_id]
    
    def clear_session(self, session_id: str) -> None:
        """Clear a specific session."""
        if session_id in self.sessions:
            self.sessions[session_id].clear()
    
    def clear_all_sessions(self) -> None:
        """Clear all sessions."""
        for session in self.sessions.values():
            session.clear()

# Global memory manager
memory_manager = MemoryManager() 