#!/usr/bin/env python3
"""
Startup script for ContextAgent
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

def check_environment():
    """Check if required environment variables are set."""
    load_dotenv()
    
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Please create a .env file with your API keys:")
        print("   cp env.example .env")
        print("   # Then edit .env and add your OpenAI API key")
        return False
    
    print("✅ Environment variables configured")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import fastapi
        import langchain
        import openai
        import chromadb
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Please install dependencies:")
        print("   pip install -r requirements.txt")
        return False

def main():
    """Main startup function."""
    print("🚀 Starting ContextAgent...")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\n🎯 Starting server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("🧪 Test Script: python test_api.py")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 