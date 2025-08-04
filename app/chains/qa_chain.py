from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import Document
from app.ingest.vector_store import vector_store
from app.memory.session_memory import memory_manager
from app.utils.config import settings

class QAChain:
    """RAG-based question answering chain."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_MODEL,
            temperature=0.7
        )
        self.chain = None
        self._initialize_chain()
    
    def _initialize_chain(self):
        """Initialize the conversational retrieval chain."""
        # Create a retriever from the vector store
        retriever = vector_store.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        # Create the conversational chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            return_source_documents=True,
            verbose=False
        )
    
    def get_answer(self, question: str, session_id: str = "default") -> Dict[str, Any]:
        """Get an answer using RAG pipeline."""
        try:
            # Get session memory
            session_memory = memory_manager.get_session(session_id)
            
            # Get conversation history
            chat_history = session_memory.get_messages()
            
            # Run the chain
            result = self.chain({
                "question": question,
                "chat_history": chat_history
            })
            
            # Extract source documents
            source_docs = result.get("source_documents", [])
            sources = []
            for doc in source_docs:
                if hasattr(doc, 'metadata') and doc.metadata:
                    source = doc.metadata.get('source', 'unknown')
                    if source not in sources:
                        sources.append(source)
            
            # Add to memory
            session_memory.add_message("user", question)
            session_memory.add_message("agent", result["answer"])
            
            return {
                "answer": result["answer"],
                "sources": sources,
                "metadata": {
                    "model": settings.OPENAI_MODEL,
                    "session_id": session_id,
                    "documents_retrieved": len(source_docs)
                }
            }
            
        except Exception as e:
            return {
                "answer": f"I encountered an error while processing your question: {str(e)}",
                "sources": [],
                "metadata": {
                    "error": str(e),
                    "session_id": session_id
                }
            }
    
    def get_simple_answer(self, question: str) -> str:
        """Get a simple answer without conversation history."""
        try:
            # Get relevant documents
            relevant_docs = vector_store.get_relevant_documents(question)
            
            if not relevant_docs:
                return "I don't have any relevant documents to answer your question. Please upload some documents first."
            
            # Create context from documents
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Create prompt
            prompt = f"""Based on the following context, answer the question. If the answer cannot be found in the context, say so.

Context:
{context}

Question: {question}

Answer:"""
            
            # Get response from LLM
            response = self.llm.invoke(prompt)
            
            return response.content
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"

# Global QA chain instance
qa_chain = QAChain() 