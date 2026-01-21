"""
FastAPI Server for Diligent-Jarvis AI Assistant
Provides REST endpoints for chat functionality and knowledge management
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import time
import os

from backend.config import get_settings, Settings
from backend.llm_handler import get_llm_handler, LLMHandler
from backend.vector_db import get_vector_db, VectorDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("jarvis_api")

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Enterprise AI Assistant API with RAG capabilities"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---

class ChatRequest(BaseModel):
    message: str
    use_context: bool = True
    stream: bool = False

class ChatResponse(BaseModel):
    response: str
    context_used: bool
    processing_time: float

class KnowledgeRequest(BaseModel):
    text: str
    metadata: Optional[Dict[str, Any]] = None

class KnowledgeResponse(BaseModel):
    status: str
    id: str
    message: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

class HealthResponse(BaseModel):
    status: str
    components: Dict[str, bool]
    version: str

# --- Endpoints ---

@app.get("/health", response_model=HealthResponse)
def health_check(
    llm: LLMHandler = Depends(get_llm_handler),
    vdb: VectorDatabase = Depends(get_vector_db)
):
    """System health check"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "components": {
            "llm_engine": llm.is_ready(),
            "vector_db": vdb.is_connected
        }
    }

@app.post("/chat")
def chat_endpoint(
    request: ChatRequest,
    llm: LLMHandler = Depends(get_llm_handler),
    vdb: VectorDatabase = Depends(get_vector_db)
):
    """
    Main chat endpoint. Supports RAG and optional streaming.
    Defined as sync (def) to run in threadpool and avoid blocking event loop.
    """
    start_time = time.time()
    
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # 1. Retrieve Context
    context = ""
    if request.use_context and vdb.is_connected:
        context = vdb.get_context_for_query(request.message)
        logger.info(f"Retrieved context length: {len(context)}")

    # 2. Streaming Response
    if request.stream:
        # The generator runs in the response processing
        return StreamingResponse(
            llm.generate_stream(request.message, context),
            media_type="text/event-stream"
        )

    # 3. Standard Response
    response_text = llm.generate_response(request.message, context)
    
    processing_time = time.time() - start_time
    
    return {
        "response": response_text,
        "context_used": bool(context),
        "processing_time": processing_time
    }

@app.post("/knowledge", response_model=KnowledgeResponse)
def add_knowledge(
    request: KnowledgeRequest,
    vdb: VectorDatabase = Depends(get_vector_db)
):
    """Add new knowledge to the vector database"""
    if not vdb.is_connected:
        raise HTTPException(status_code=503, detail="Vector DB not available")
        
    try:
        doc_id = vdb.store_knowledge(request.text, request.metadata)
        return {
            "status": "success",
            "id": doc_id,
            "message": "Knowledge successfully ingested"
        }
    except Exception as e:
        logger.error(f"Knowledge ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
def search_knowledge(
    request: SearchRequest,
    vdb: VectorDatabase = Depends(get_vector_db)
):
    """Debug endpoint to search the knowledge base directly"""
    if not vdb.is_connected:
        raise HTTPException(status_code=503, detail="Vector DB not available")
        
    results = vdb.search_similar(request.query, request.top_k)
    return {"results": results, "count": len(results)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.api:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )