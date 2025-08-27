# 🤖 ContextAgent

A modular, production-ready AI assistant backend built with **Python**, **LangChain**, **OpenAI API**, and **RAG (Retrieval-Augmented Generation)** pipeline.

## ✨ Features

- 🔍 **RAG Pipeline**: Embed documents and perform similarity search for context retrieval
- 🤖 **LangChain Agent**: Chain of tools including Calculator and Google Search
- 💬 **Conversational Memory**: Maintains conversation history using LangChain's ConversationBufferMemory
- 🧾 **Document Ingestion**: Support for PDFs, TXT, Markdown, and DOCX files
- 🛠️ **Embeddings**: OpenAI embeddings for document vectorization
- 🗂️ **Vector Store**: ChromaDB for fast document retrieval
- 🔑 **Environment-based Configuration**: Secure API key management
- 📄 **Swagger Documentation**: Auto-generated API docs
- 🚀 **FastAPI Backend**: High-performance async API

## 🏗️ Architecture

```
ContextAgent/
├── app/
│   ├── main.py                # FastAPI app entrypoint
│   ├── routes/
│   │   ├── chat.py            # Chat endpoints
│   │   └── ingest.py          # Document upload endpoints
│   ├── chains/
│   │   ├── qa_chain.py        # RAG + LLM chain
│   │   └── agent_chain.py     # LangChain agent setup
│   ├── tools/
│   │   ├── calculator.py      # Custom LangChain tools
│   │   └── google_search.py   # Web search tool
│   ├── memory/
│   │   └── session_memory.py  # Conversational memory
│   ├── ingest/
│   │   ├── embedder.py        # Embedding function
│   │   └── vector_store.py    # ChromaDB setup
│   ├── utils/
│   │   ├── config.py          # Environment + settings
│   │   └── document_loader.py # Document processing
│   └── schemas/
│       └── request_model.py   # Pydantic schemas
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone git https://github.com:webcodelabb/ContextAgent.git
cd ContextAgent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the example environment file and add your API keys:

```bash
cp env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
```

### 4. Run the Application

```bash
python -m app.main
```

The server will start at `http://localhost:8000`

## 📚 API Documentation

### Chat Endpoints

#### `POST /chat/`

Ask questions to the AI assistant.

**Request Body:**
```json
{
  "question": "What does this PDF say about climate change?",
  "history": [
    {"role": "user", "content": "Summarize the document"},
    {"role": "agent", "content": "Sure, here's the summary..."}
  ],
  "use_rag": true,
  "use_agent": false
}
```

**Response:**
```json
{
  "answer": "The PDF discusses the recent changes in global temperatures and the effects of greenhouse gases...",
  "sources": ["climate_report_2024.pdf"],
  "reasoning": null,
  "metadata": {
    "model": "gpt-4",
    "session_id": "default",
    "documents_retrieved": 3
  }
}
```

#### `GET /chat/memory/{session_id}`

Get conversation history for a session.

#### `DELETE /chat/memory/{session_id}`

Clear conversation memory for a session.

#### `GET /chat/tools`

Get information about available tools.

#### `GET /chat/stats`

Get statistics about the chat system.

### Document Ingestion Endpoints

#### `POST /ingest/upload`

Upload a document for processing.

**Supported formats:** PDF, TXT, MD, DOCX

#### `POST /ingest/directory`

Ingest all supported documents from a directory.

#### `GET /ingest/stats`

Get statistics about ingested documents.

#### `DELETE /ingest/clear`

Clear all ingested documents.

### Health Check

#### `GET /` or `GET /health`

Check system health and configuration.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4` |
| `VECTOR_STORE_TYPE` | Vector store type | `chroma` |
| `CHROMA_PERSIST_DIRECTORY` | ChromaDB storage path | `./chroma_db` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `SERP_API_KEY` | SerpAPI key for web search | - |
| `LANGCHAIN_TRACING_V2` | Enable LangSmith tracing | `false` |
| `LANGCHAIN_API_KEY` | LangSmith API key | - |

## 🛠️ Usage Examples

### Python Client

```python
import requests

# Chat with RAG
response = requests.post("http://localhost:8000/chat/", json={
    "question": "What are the main points in the uploaded documents?",
    "use_rag": True
})
print(response.json()["answer"])

# Chat with Agent
response = requests.post("http://localhost:8000/chat/", json={
    "question": "What's 15 * 23?",
    "use_agent": True
})
print(response.json()["answer"])
```

### cURL Examples

```bash
# Simple chat
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello, how are you?"}'

# Upload document
curl -X POST "http://localhost:8000/ingest/upload" \
  -F "file=@document.pdf"

# Get system stats
curl "http://localhost:8000/chat/stats"
```

## 🧪 Testing

### Manual Testing

1. Start the server: `python -m app.main`
2. Open Swagger docs: `http://localhost:8000/docs`
3. Test endpoints through the interactive interface

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# Upload a test document
curl -X POST "http://localhost:8000/ingest/upload" \
  -F "file=@test_document.pdf"

# Ask a question
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

## 🔍 Features in Detail

### RAG Pipeline

1. **Document Ingestion**: Upload PDFs, TXTs, MDs, DOCXs
2. **Text Processing**: Split documents into chunks
3. **Embedding**: Convert text to vectors using OpenAI
4. **Storage**: Store in ChromaDB vector database
5. **Retrieval**: Find relevant documents for queries
6. **Generation**: Generate answers using LLM with context

### LangChain Agent

- **Calculator Tool**: Perform mathematical calculations
- **Google Search Tool**: Search the web for current information
- **Conversational Memory**: Maintains chat history
- **Multi-step Reasoning**: Chain multiple tools together

### Document Processing

- **PDF**: PyPDF2 for text extraction
- **TXT**: UTF-8 text files
- **MD**: Markdown files
- **DOCX**: Microsoft Word documents
- **Chunking**: Intelligent text splitting with overlap
- **Metadata**: Preserves source information

## 🚀 Production Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup

```bash
# Production environment
export OPENAI_API_KEY=your_production_key
export OPENAI_MODEL=gpt-4
export HOST=0.0.0.0
export PORT=8000
```

### Security Considerations

- Set up proper CORS configuration
- Use environment variables for secrets
- Implement authentication if needed
- Monitor API usage and costs
- Set up logging and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the amazing LLM framework
- [OpenAI](https://openai.com/) for the GPT models
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
.
---

**Built with ❤️ for Muhammad Aminu Umar** 
 
