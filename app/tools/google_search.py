from typing import Any, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from serpapi import GoogleSearch
from app.utils.config import settings

class SearchInput(BaseModel):
    """Input schema for search tool."""
    query: str = Field(..., description="Search query to look up on the web")

class GoogleSearchTool(BaseTool):
    """Google search tool using SerpAPI."""
    
    name = "google_search"
    description = "Useful for searching the web for current information. Input should be a search query."
    args_schema = SearchInput
    
    def __init__(self):
        super().__init__()
        self.api_key = settings.SERP_API_KEY
    
    def _run(self, query: str) -> str:
        """Perform a web search."""
        if not self.api_key:
            return "Error: SERP_API_KEY not configured. Please set your SerpAPI key in the environment variables."
        
        try:
            search = GoogleSearch({
                "q": query,
                "api_key": self.api_key,
                "num": 3  # Limit to 3 results
            })
            results = search.get_dict()
            
            if "organic_results" in results:
                search_results = []
                for result in results["organic_results"][:3]:
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    link = result.get("link", "")
                    search_results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")
                
                return "\n".join(search_results)
            else:
                return f"No search results found for: {query}"
                
        except Exception as e:
            return f"Error performing search for '{query}': {str(e)}"
    
    def _arun(self, query: str) -> str:
        """Async version of the search tool."""
        return self._run(query)

# Global search tool instance (only created if API key is available)
search_tool = None
if settings.SERP_API_KEY:
    search_tool = GoogleSearchTool() 