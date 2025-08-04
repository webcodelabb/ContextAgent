#!/usr/bin/env python3
"""
Test script for ContextAgent API
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json()['status']}")
            print(f"   Components: {response.json()['components']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_chat():
    """Test chat endpoint."""
    print("\n💬 Testing chat endpoint...")
    try:
        # Test simple chat
        response = requests.post(f"{BASE_URL}/chat/", json={
            "question": "Hello! Can you tell me about yourself?",
            "use_rag": False,
            "use_agent": False
        })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat test passed")
            print(f"   Answer: {result['answer'][:100]}...")
        else:
            print(f"❌ Chat test failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Chat test error: {e}")

def test_agent():
    """Test agent with calculator tool."""
    print("\n🤖 Testing agent with calculator...")
    try:
        response = requests.post(f"{BASE_URL}/chat/", json={
            "question": "What is 15 * 23? Please calculate this for me.",
            "use_agent": True
        })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Agent test passed")
            print(f"   Answer: {result['answer']}")
            if result.get('reasoning'):
                print(f"   Reasoning: {result['reasoning']}")
        else:
            print(f"❌ Agent test failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Agent test error: {e}")

def test_stats():
    """Test stats endpoint."""
    print("\n📊 Testing stats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/chat/stats")
        if response.status_code == 200:
            result = response.json()
            print("✅ Stats test passed")
            print(f"   Vector store: {result['vector_store']}")
            print(f"   Memory sessions: {result['memory_sessions']}")
            print(f"   Available tools: {result['available_tools']}")
        else:
            print(f"❌ Stats test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stats test error: {e}")

def test_tools():
    """Test tools endpoint."""
    print("\n🛠️ Testing tools endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/chat/tools")
        if response.status_code == 200:
            result = response.json()
            print("✅ Tools test passed")
            print(f"   Available tools: {result['total_tools']}")
            for tool in result['tools']:
                print(f"   - {tool['name']}: {tool['description']}")
        else:
            print(f"❌ Tools test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Tools test error: {e}")

def main():
    """Run all tests."""
    print("🚀 Starting ContextAgent API tests...")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    test_health()
    test_chat()
    test_agent()
    test_stats()
    test_tools()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\n💡 To test document upload and RAG:")
    print("   1. Upload a document via POST /ingest/upload")
    print("   2. Ask questions with use_rag=true")
    print("   3. Check the interactive docs at http://localhost:8000/docs")

if __name__ == "__main__":
    main() 