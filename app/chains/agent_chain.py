from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import BaseTool
from langchain.memory import ConversationBufferMemory
from app.tools.calculator import calculator_tool
from app.tools.google_search import search_tool
from app.utils.config import settings

class AgentChain:
    """LangChain agent with multiple tools for advanced reasoning."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_MODEL,
            temperature=0.7
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.tools = self._initialize_tools()
        self.agent = self._initialize_agent()
    
    def _initialize_tools(self) -> List[BaseTool]:
        """Initialize available tools."""
        tools = [calculator_tool]
        
        # Add search tool if API key is available
        if search_tool:
            tools.append(search_tool)
        
        return tools
    
    def _initialize_agent(self):
        """Initialize the LangChain agent."""
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=5
        )
    
    def get_answer(self, question: str, session_id: str = "default") -> Dict[str, Any]:
        """Get an answer using the agent with tools."""
        try:
            # Run the agent
            result = self.agent.invoke({"input": question})
            
            # Extract reasoning if available
            reasoning = None
            if hasattr(result, 'intermediate_steps'):
                steps = result.get('intermediate_steps', [])
                if steps:
                    reasoning = "Agent used the following tools:\n"
                    for step in steps:
                        tool_name = step[0].name if hasattr(step[0], 'name') else "Unknown tool"
                        reasoning += f"- {tool_name}\n"
            
            return {
                "answer": result["output"],
                "reasoning": reasoning,
                "metadata": {
                    "model": settings.OPENAI_MODEL,
                    "session_id": session_id,
                    "agent_type": "conversational_react",
                    "tools_used": len(self.tools)
                }
            }
            
        except Exception as e:
            return {
                "answer": f"I encountered an error while processing your question: {str(e)}",
                "reasoning": None,
                "metadata": {
                    "error": str(e),
                    "session_id": session_id
                }
            }
    
    def get_tools_info(self) -> List[Dict[str, str]]:
        """Get information about available tools."""
        tools_info = []
        for tool in self.tools:
            tools_info.append({
                "name": tool.name,
                "description": tool.description
            })
        return tools_info

# Global agent chain instance
agent_chain = AgentChain() 