# Diligent Jarvis

> **Enterprise-Grade Neural Interface**
> A self-hosted, RAG-enabled AI assistant featuring a cutting-edge React frontend and local LLM inference.

![Status](https://img.shields.io/badge/status-online-success)
![License](https://img.shields.io/badge/license-MIT-blue)

## Overview

Diligent Jarvis is a locally-deployed AI platform that bridges the gap between secure, offline inference and modern, high-fidelity user experiences. It implements Retrieval-Augmented Generation (RAG) to provide context-aware responses using your own data, all without sending a single byte to external cloud providers.

**Key Features:**
- **Local Inference:** Runs quantized LLaMA/Mistral models via `llama-cpp-python`.
- **Neural Interface:** A "Billion Dollar" UI built with React, Vite, TailwindCSS, and Framer Motion.
- **RAG Memory Bank:** Ingest documents into a local Pinecone vector store for semantic retrieval.
- **Real-Time Streaming:** Server-Sent Events (SSE) for low-latency token generation.
- **Cyberpunk Aesthetic:** Glassmorphic design, scanlines, and reactive animations.

## Architecture

The system follows a decoupled microservices architecture:

### 🧠 Backend (FastAPI)
- **Port:** `8000`
- **Stack:** Python 3.11, FastAPI, LangChain, Pinecone
- **Role:** Handles model inference, vector embedding, and context retrieval.

### 🖥️ Frontend (React)
- **Port:** `5173`
- **Stack:** React 18, Vite, Tailwind CSS, Lucide React
- **Role:** Provides the immersive, responsive user interface.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Jai3405/Diligent-Jarvis.git
cd Diligent-Jarvis
```

### 2. Backend Setup
Install Python dependencies and download a model.

```bash
# Install dependencies
pip install -r requirements.txt

# Download a model (Example: TinyLlama for speed)
mkdir models
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -P models/
```

### 3. Environment Configuration
Create a `.env` file in the root directory:

```env
# App Settings
APP_NAME=Diligent-Jarvis
VERSION=2.0.0
DEBUG=True

# Model Settings
MODEL_PATH=models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
MODEL_TYPE=llama
MAX_TOKENS=1024

# Pinecone (Vector DB)
PINECONE_API_KEY=your_api_key_here
PINECONE_INDEX_NAME=jarvis-memory
PINECONE_REGION=us-east-1
```

### 4. Frontend Setup
Install Node.js dependencies.

```bash
cd frontend
npm install
cd ..
```

## Running the System

Open **two terminal windows** to run the services side-by-side.

**Terminal 1: Backend**
```bash
./start_backend.sh
```

**Terminal 2: Frontend**
```bash
./start_frontend.sh
```

Access the Neural Interface at: **http://localhost:5173**

## Usage Guide

### 💬 Neural Chat
- **RAG Mode:** Toggle the "RAG Retrieval" switch to enable context-aware answers.
- **Streaming:** Toggle "Stream" to see the AI think in real-time.

### 🧠 Memory Bank
1. Navigate to the **Memory Bank** tab.
2. Paste text content (e.g., reports, emails, docs).
3. Assign a source ID.
4. Click **Process & Embed**.
5. The system now "knows" this information and will use it in future chats.

## Project Structure

```
Diligent-Jarvis/
├── backend/                 # FastAPI Logic
│   ├── api.py              # Endpoints
│   ├── llm_handler.py      # LLaMA Inference Engine
│   └── vector_db.py        # Pinecone Integration
├── frontend/                # React Application
│   ├── src/
│   │   ├── components/     # UI Components (Chat, Sidebar, etc.)
│   │   ├── lib/            # API Clients
│   │   └── App.jsx         # Main Entry
│   └── tailwind.config.js  # Styling Config
├── tests/                   # Pytest Suite
└── requirements.txt         # Dependencies
```

## Technical Highlights
- **Vector Search:** Uses `all-MiniLM-L6-v2` for high-quality embeddings.
- **Optimized Inference:** Configured for `n_batch=512` and multi-threaded CPU processing.
- **Reactive UI:** Framer Motion handles all UI transitions for a premium feel.

---
**Author:** Jai3405
**License:** MIT
