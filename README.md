# Diligent Jarvis

> A self-hosted RAG-enabled conversational AI system built with enterprise-grade architecture principles.

## Overview

Diligent Jarvis is a locally-deployed language model interface that implements Retrieval-Augmented Generation (RAG) to provide context-aware responses. The system follows a microservices architecture, decoupling the inference engine from the user interface to enable independent scaling and deployment flexibility.

**Key Features:**
- Self-hosted LLM inference using quantized GGUF models
- Semantic search via Pinecone vector database
- Real-time streaming responses with Server-Sent Events
- Modern glassmorphic UI with zero framework dependencies
- Complete data sovereignty - no external API calls for inference

## Architecture

The system is split into two independent services:

### Backend Service (Port 8000)
**Technology:** FastAPI + llama-cpp-python

The backend handles all compute-intensive operations:
- **Model Inference**: Runs quantized LLaMA models via llama.cpp bindings
- **Vector Operations**: Manages embeddings generation and similarity search
- **Context Retrieval**: Implements RAG pipeline for knowledge-augmented responses
- **Streaming**: Supports token-by-token streaming for real-time UX

Key implementation details:
- Asynchronous request handling with FastAPI
- Singleton pattern for model loading (reduces memory footprint)
- Dynamic prompt formatting based on model type (ChatML vs LLaMA-2 format)
- Thread-pool optimization for CPU-bound inference tasks

### Frontend Service (Port 8080)
**Technology:** Vanilla JavaScript (ES6+)

A lightweight single-page application:
- Pure JavaScript implementation - no React, Vue, or Angular dependencies
- Server-Sent Events (SSE) for streaming response handling
- Glassmorphism design system with CSS custom properties
- Lucide icons for consistent vector graphics

## Installation & Setup

### 1. Clone and Install Dependencies

```bash
git clone https://github.com/Jai3405/Diligent-Jarvis.git
cd Diligent-Jarvis
pip install -r requirements.txt
```

### 2. Download a Language Model

Download a GGUF-format model from HuggingFace. Recommended options:

**For Testing (Fast):**
```bash
# TinyLlama - 1.1B parameters, ~637MB
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -P models/
```

**For Production (Better Quality):**
```bash
# LLaMA-2 7B - ~3.8GB
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf -P models/
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and set:
```env
# Point to your downloaded model
MODEL_PATH=models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

# Add your Pinecone credentials
PINECONE_API_KEY=your_api_key_here
PINECONE_INDEX_NAME=jarvis-knowledge
PINECONE_REGION=us-east-1
```

**Getting Pinecone API Key:**
1. Sign up at [pinecone.io](https://www.pinecone.io/)
2. Create a new project
3. Copy API key from dashboard
4. The index will be auto-created on first run

### 4. Launch the Application

Open **two terminal windows** and run:

**Terminal 1 - Backend:**
```bash
bash start_backend.sh
# Wait for: "Model loaded successfully!"
```

**Terminal 2 - Frontend:**
```bash
bash start_frontend.sh
# Server starts at http://localhost:8080
```

Access the interface at: **http://localhost:8080**

## Usage Guide

### Basic Chat
1. Type your question in the input box
2. Press Enter or click the send button
3. Toggle "Stream" for token-by-token responses

### Knowledge Base (RAG)
1. Click "Memory Bank" in the sidebar
2. Paste text content you want the AI to remember
3. Add a source identifier (e.g., "Project Documentation")
4. Click "Process & Embed"
5. Future queries will retrieve relevant context automatically

**How RAG Works:**
- Your text is chunked and converted to vector embeddings
- Stored in Pinecone with metadata
- When you ask questions, semantic search finds relevant chunks
- Retrieved context is injected into the LLM prompt
- Model generates answers grounded in your data

### API Endpoints

The backend exposes REST endpoints for integration:

```bash
# Health check
curl http://localhost:8000/health

# Chat completion
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "use_context": true, "stream": false}'

# Add knowledge
curl -X POST http://localhost:8000/knowledge \
  -H "Content-Type: application/json" \
  -d '{"text": "Important information", "metadata": {"source": "docs"}}'
```

## Technical Stack

### Backend
- **FastAPI**: ASGI web framework for high-performance APIs
- **llama-cpp-python**: Python bindings for llama.cpp (C++ inference engine)
- **Pinecone**: Managed vector database for semantic search
- **sentence-transformers**: Embedding model (all-MiniLM-L6-v2)
- **Pydantic**: Data validation and settings management

### Frontend
- **Vanilla JavaScript**: No framework overhead
- **Marked.js**: Markdown parser for formatted responses
- **Lucide**: Feather-style icon library
- **CSS Grid/Flexbox**: Modern layout system

### Architecture Patterns
- **Microservices**: Independent backend and frontend services
- **Singleton Pattern**: Single model instance shared across requests
- **Async/Await**: Non-blocking I/O for concurrent request handling
- **Streaming**: Server-Sent Events for real-time response delivery

## Project Structure

```
Diligent-Jarvis/
├── backend/
│   ├── main.py              # FastAPI application & routes
│   ├── llm_handler.py       # Model loading & inference logic
│   ├── vector_db.py         # Pinecone integration & RAG pipeline
│   └── config.py            # Environment configuration
├── frontend/
│   ├── index.html           # Single-page application
│   ├── script.js            # UI logic & API calls
│   └── style.css            # Glassmorphic design system
├── models/                  # GGUF model files (gitignored)
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── start_backend.sh         # Backend launch script
└── start_frontend.sh        # Frontend launch script
```

## Performance Considerations

**Model Selection Trade-offs:**
- **TinyLlama (1.1B)**: Fast inference (~1-2 tokens/sec on CPU), lower quality
- **LLaMA-2 7B**: Better responses (~0.5 tokens/sec on CPU), requires 8GB RAM
- **Quantization**: Q4_K_M offers best quality/size ratio for 4-bit quantized models

**Scaling:**
- Backend can run on CPU (slower) or GPU (fast)
- Frontend is stateless and can be served via CDN
- Pinecone handles vector operations at scale

## Development Notes

This project was built to demonstrate understanding of:
- RAG architecture and vector search fundamentals
- Asynchronous Python with FastAPI
- Efficient LLM inference on consumer hardware
- Modern frontend development without framework dependencies
- Microservices design patterns

**Design Decisions:**
- Chose llama.cpp over Hugging Face Transformers for better CPU performance
- Used Pinecone over local vector stores (Chroma/FAISS) for production-ready scalability
- Implemented prompt template switching to support multiple model formats
- Vanilla JS frontend to minimize bundle size and improve load times

---

**License:** MIT
**Author:** Jai3405