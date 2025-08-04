from typing import Any
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import re
import math

class CalculatorInput(BaseModel):
    """Input schema for calculator tool."""
    expression: str = Field(..., description="Mathematical expression to evaluate")

class CalculatorTool(BaseTool):
    """Custom calculator tool for mathematical operations."""
    
    name = "calculator"
    description = "Useful for performing mathematical calculations. Input should be a valid mathematical expression."
    args_schema = CalculatorInput
    
    def _run(self, expression: str) -> str:
        """Evaluate a mathematical expression safely."""
        try:
            # Clean the expression
            expression = expression.strip()
            
            # Remove any potentially dangerous characters
            expression = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            
            # Evaluate the expression
            result = eval(expression)
            
            # Format the result
            if isinstance(result, (int, float)):
                if result == int(result):
                    return str(int(result))
                else:
                    return f"{result:.4f}"
            else:
                return str(result)
                
        except Exception as e:
            return f"Error calculating '{expression}': {str(e)}"
    
    def _arun(self, expression: str) -> str:
        """Async version of the calculator tool."""
        return self._run(expression)

# Global calculator tool instance
calculator_tool = CalculatorTool() 