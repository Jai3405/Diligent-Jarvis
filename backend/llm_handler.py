"""
LLM Handler for running self-hosted language models
Uses LLaMA model with llama-cpp-python for efficient inference
"""

from llama_cpp import Llama
from typing import Optional, Dict, List, Generator
from backend.config import get_settings
import os
import logging
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

class LLMHandler:
    """Manages LLaMA model loading and inference"""

    def __init__(self):
        """Initialize LLaMA model"""
        self.model: Optional[Llama] = None
        self.model_loaded = False
        self._load_model()

    def _load_model(self):
        """Load the LLaMA model from disk"""
        try:
            if not os.path.exists(settings.MODEL_PATH):
                logger.warning(f"Model file not found at {settings.MODEL_PATH}")
                logger.warning("Please download a GGUF model file and update MODEL_PATH in .env")
                return

            logger.info(f"Loading LLaMA model from {settings.MODEL_PATH}...")
            
            # Initialize with optimized parameters
            self.model = Llama(
                model_path=settings.MODEL_PATH,
                n_ctx=settings.CONTEXT_WINDOW,
                n_threads=os.cpu_count() or 4,
                n_batch=512,
                verbose=False
            )

            self.model_loaded = True
            logger.info("Model loaded successfully!")

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model_loaded = False

    def generate_stream(
        self,
        prompt: str,
        context: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> Generator[str, None, None]:
        """
        Generate a streaming response using the LLaMA model
        """
        if not self.model_loaded or not self.model:
            yield "Error: Model not loaded. Please check server logs."
            return

        full_prompt = self._build_prompt(prompt, context)
        
        try:
            stream = self.model(
                full_prompt,
                max_tokens=max_tokens or settings.MAX_TOKENS,
                temperature=temperature or settings.TEMPERATURE,
                stop=["</s>", "User:", "Human:", "[INST]"],
                stream=True,
                echo=False
            )

            for output in stream:
                token = output['choices'][0]['text']
                yield token

        except Exception as e:
            logger.error(f"Error during generation: {e}")
            yield "I encountered an error generating the response."

    def generate_response(
        self,
        prompt: str,
        context: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Generate a complete response (blocking)
        """
        if not self.model_loaded or not self.model:
            return "Error: Model not loaded."

        full_prompt = self._build_prompt(prompt, context)

        try:
            response = self.model(
                full_prompt,
                max_tokens=max_tokens or settings.MAX_TOKENS,
                temperature=temperature or settings.TEMPERATURE,
                stop=["</s>", "User:", "Human:", "[INST]"],
                echo=False
            )
            return response['choices'][0]['text'].strip()

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I encountered an error."

    def _build_prompt(self, user_query: str, context: Optional[str] = None) -> str:
        """
        Build a properly formatted prompt based on the model type
        """
        model_path_lower = settings.MODEL_PATH.lower()
        is_tinyllama = "tinyllama" in model_path_lower

        system_message = """You are Jarvis, an advanced enterprise AI assistant.
Your goal is to provide accurate, professional, and concise assistance.
When context is provided, prioritize it over your internal knowledge.
If the context doesn't contain the answer, say so politely.
Always maintain a helpful and professional tone."""

        # 1. TinyLlama Format (ChatML-style)
        if is_tinyllama:
            prompt = f"<|system|>\n{system_message}</s>\n"
            
            if context:
                prompt += f"<|user|>\nContext Data:\n{context}\n\nQuestion: {user_query}</s>\n"
            else:
                prompt += f"<|user|>\n{user_query}</s>\n"
                
            prompt += "<|assistant|>\n"
            return prompt

        # 2. LLaMA-2 / Mistral Format (Default)
        if context:
            prompt = f"""[INST] <<SYS>>
{system_message}

CONTEXT DATA:
{context}
<</SYS>>

Based on the context above, please answer: {user_query} [/INST]"""
        else:
            prompt = f"""[INST] <<SYS>>
{system_message}
<</SYS>>

{user_query} [/INST]"""

        return prompt

    def is_ready(self) -> bool:
        return self.model_loaded

# Global singleton (loaded on module import, or could be lazy loaded)
# For this scale, a simple singleton pattern works well.
llm_instance = LLMHandler()

def get_llm_handler() -> LLMHandler:
    return llm_instance