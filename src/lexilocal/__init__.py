"""
LexiLocal: AI-Powered Legal Document Analysis

A comprehensive legal document analysis system using local LLMs,
RAG (Retrieval-Augmented Generation), and quantized model optimization.
"""

__version__ = "1.0.0"
__author__ = "Dylan Satow"
__email__ = "your.email@example.com"

from .core.rag_system import LegalRAGSystem
from .core.document_processor import DocumentProcessor
from .data.mock_data import get_mock_dataset

__all__ = [
    "LegalRAGSystem",
    "DocumentProcessor", 
    "get_mock_dataset"
]